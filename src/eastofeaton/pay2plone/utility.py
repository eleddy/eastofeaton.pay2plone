from persistent.mapping import PersistentMapping
from persistent.list import PersistentList
from zope.interface import implements
from zope.container.ordered import OrderedContainer

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility

# from eastofeaton.pay2plone.interfaces import ISiteTemplate
# from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry

_marker = object()


class Pay2PloneUtility(OrderedContainer):
    """ a persistent utility stores information about purchased sites

        keys are member ids
        values are persistent dicts, like so:
        
        P2PUtility
         |- member1 -> PersistentDict
                        |- 'active' -> PersistentList
                                        |- SiteRecord
                        |- 'inactive' -> PersistentList
                                        |- SiteRecord
    """
    implements(IPay2PloneUtility)

    def get_user_record(self, member_id):
        if member_id not in self:
            user_record = PersistentMapping()
            user_record['active'] = PersistentList()
            user_record['inactive'] = PersistentList()
            self[member_id] = user_record

        return self[member_id]

