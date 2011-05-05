# from persistent.mapping import PersistentMapping
# from persistent.list import PersistentList
from zope.interface import implements
from zope.container.ordered import OrderedContainer
from zope.container.contained import NameChooser
from zope.container.interfaces import INameChooser
from zope.container.constraints import checkObject

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility
from eastofeaton.pay2plone.interfaces import IPay2PloneUserRecord

# from eastofeaton.pay2plone.interfaces import ISiteTemplate
# from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry

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

