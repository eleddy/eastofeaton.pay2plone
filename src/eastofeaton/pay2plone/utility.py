# from persistent.mapping import PersistentMapping
# from persistent.list import PersistentList
from Acquisition import aq_parent
from Acquisition import aq_inner
from AccessControl.SecurityManagement import newSecurityManager

from zope.interface import implements
from zope.container.ordered import OrderedContainer
from zope.container.contained import NameChooser
from zope.container.interfaces import INameChooser
from zope.container.constraints import checkObject
from zope.component.hooks import getSite
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

# from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.factory import addPloneSite
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility
from eastofeaton.pay2plone.interfaces import IPay2PloneUserRecord
from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry


_marker = object()


class SiteRecordNameChooser(NameChooser):
    
    implements(INameChooser)
    
    def __init__(self, context):
        self.context = context
    


class Pay2PloneUserRecord(OrderedContainer):
    """ stores individual site purchase records for a user
    """
    implements(IPay2PloneUserRecord)

    def add_site_record(self, site_record):
        orig_name = site_record.id
        chooser = INameChooser(self)
        try:
            chooser.checkName(orig_name, site_record)
        except KeyError:
            # the name already exists, no problem, we're just going to 
            # increment it anyway
            pass
        except (TypeError, ValueError):
            msg = "%s is not useable as a name for a site record" % orig_name
            raise ValueError(msg)

        name = chooser.chooseName(orig_name, site_record)
        checkObject(self, name, site_record)
        site_record.id = name
        self[name] = site_record
        return name

    def get_site_record(self, record_id):
        if record_id not in self:
            return None
        return self[record_id]

    def delete_site_record(self, record_id):
        if record_id not in self:
            return
        del self[record_id]


class Pay2PloneUtility(OrderedContainer):
    """ a persistent utility stores information about purchased sites

        keys are member ids
        values are persistent dicts, like so:
        
        P2PUtility
         |- member1 -> PersistentDict
                        |- 'site_id' -> SiteRecord
    """
    implements(IPay2PloneUtility)

    def get_user_record(self, member_id):
        if member_id not in self:
            user_record = Pay2PloneUserRecord()
            self[member_id] = user_record

        return self[member_id]

    def create_site_for(self, site_record, member_id):
        if site_record.is_expired() or site_record.created:
            raise ValueError('This site record is expired or already exists')

        t_registry = queryUtility(ISiteTemplateRegistry, default=_marker)
        if t_registry is _marker:
            raise ValueError('Template Registry cannot be found')

        extension_profiles = ['plonetheme.sunburst:default',]
        template_id = site_record.template
        template = t_registry.get_template_by_id(template_id)
        normalizer = queryUtility(IIDNormalizer, default=_marker)
        newsite_id = normalizer.normalize(site_record.id)
        add_ons = list(template.products)
        extension_profiles.extend(add_ons)

        portal = getSite()
        with Escalation(portal, 'admin'):
            app = aq_parent(aq_inner(portal))
            newsite = addPloneSite(app, newsite_id, title="Pay2Plone Site",
                                   extension_ids=extension_profiles)
            user_info = self._get_current_user_info(portal, member_id)
            self._add_user_to_site(newsite, **user_info)
            # TODO: copy user property sheets from old site to new
            print 'site created: %s' % newsite

        return newsite

    def _get_current_user_info(self, site, member_id):
        local_acl = site.acl_users
        user = local_acl.getUserById(member_id)
        local_plugins = local_acl._getOb('plugins')
        acl_user_info = local_acl._verifyUser(local_plugins, 
                                              user_id=user.getId())
        wanted_plugin = acl_user_info['pluginid']
        my_plugin = None
        for plugid, plugin in local_plugins.listPlugins(IUserAdderPlugin):
            if plugid == wanted_plugin:
                my_plugin = plugin
                break
            continue
        if my_plugin is None:
            msg = "unable to locate user information for %s"
            raise ValueError(msg % member_id)
        user_passwd = my_plugin._user_passwords[acl_user_info['id']]
        user_info = {'login': acl_user_info['login'],
                     'password': user_passwd}
        return user_info

    def _add_user_to_site(self, newsite, login=None, password=None):
        if not login or not password:
            msg = 'Unable to duplicate user, missing required argument'
            raise ValueError(msg)
        newsite.acl_users._doAddUser(login, password, ['Manager',], [])
        


class Escalation(object):
    """ define a context in which privileges are escalated.
        
        priveleges return to normal as soon as the context is left
    """
    
    site = None
    app = None
    escalate_to = None
    original_user = None

    def __init__(self, site, userid):
        self.site = site
        self.app = aq_parent(aq_inner(site))
        self.escalate_to = self.app.acl_users.getUserById(userid)
        mtool = self.site.portal_membership
        if mtool.isAnonymousUser():
            raise ValueError('Unable to escalate for anonymous users')
        current_userid = mtool.getAuthenticatedMember().id
        self.original_user = self.site.acl_users.getUserById(current_userid)

    def __enter__(self):
        newSecurityManager(None, 
                           self.escalate_to.__of__(self.app.acl_users))

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is not None:
            print 'There was a fuckup: %s: %s\n\n%s' % (exception_type,
                                                        exception_value,
                                                        exception_traceback)
        newSecurityManager(None, 
                           self.original_user.__of__(self.site.acl_users))

