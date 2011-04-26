from zope.component import queryUtility

from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import exportObjects

from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry

_marker = object()


class SiteTemplateRegistryXMLAdapter(XMLAdapterBase):

    __used_for__ = ISiteTemplateRegistry

    _LOGGER_ID = name = 'sitetemplateregistry'

    def _importNode(self, node):
        import pdb; pdb.set_trace( )
        print 'i am _importNode'
    
    def _exportNode(self, node):
        import pdb; pdb.set_trace( )
        print 'i am _exportNode'

def importSiteTemplateRegistry(context):
    import pdb; pdb.set_trace( )
    registry = queryUtility(ISiteTemplateRegistry, _marker)
    if registry is _marker:
        return

    print 'i am the importer'
    importObjects(registry, '', context)


def exportSiteTemplateRegistry(context):
    import pdb; pdb.set_trace( )
    registry = queryUtility(ISiteTemplateRegistry, _marker)
    if registry is _marker:
        return

    print 'i am the exporter'
    exportObjects(registry, '', context)
