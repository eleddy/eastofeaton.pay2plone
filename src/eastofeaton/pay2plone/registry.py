from zope.interface import implements
from zope.container.ordered import OrderedContainer
from zope.container.constraints import checkObject

from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry


class SiteTemplateRegistry(OrderedContainer):
    """ a registry for site template objects
    """
    implements(ISiteTemplateRegistry)

    def add_template(self, template):
        tid = template.id
        checkObject(self, tid, template)
        if tid in self:
            del self[tid]
        self[tid] = template

    def remove_template(self, tid):
        if not tid in self:
            # perhaps some sort of logged info here???
            return
        del self[tid]

    def list_templates(self):
        return self.keys()

    def get_template_by_id(self, tid):
        return self.get(tid, None)
