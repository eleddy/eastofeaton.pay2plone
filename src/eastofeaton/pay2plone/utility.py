from persistent import Persistent
# from persistent.mapping import PersistentMapping
from zope.interface import implements
# from zope.component import queryUtility
# from zope.app.component.hooks import getSite

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility
# from eastofeaton.pay2plone.interfaces import ISiteTemplate
# from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry

_marker = object()


class Pay2PloneUtility(Persistent):
    """ a persistent utility which stores configuration and user information
    """
    implements(IPay2PloneUtility)
