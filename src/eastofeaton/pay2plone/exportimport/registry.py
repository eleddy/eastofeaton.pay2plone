import os
import decimal

from zope.component import queryUtility
from zope.component import queryMultiAdapter

from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.interfaces import IBody

from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry
from eastofeaton.pay2plone.sitetemplate import SimpleSiteTemplate

_marker = object()
ALLOWED_TEMPLATE_TYPES = ['simpletemplate', ]


class SiteTemplateRegistryXMLAdapter(XMLAdapterBase):

    __used_for__ = ISiteTemplateRegistry

    _LOGGER_ID = name = 'sitetemplateregistry'

    def _importNode(self, node):
        # global purge
        purge = self.environ.shouldPurge()
        if node.getAttribute('purge'):
            purge = self._convertToBoolean(node.getAttribute('purge'))
        if purge:
            self._purgeRegistry()
        for child in node.childNodes:
            nodename = child.nodeName.lower()
            if nodename in ALLOWED_TEMPLATE_TYPES:
                purgeChild = False
                if child.getAttribute('purge'):
                    purgeChild = self._convertToBoolean(
                        child.getAttribute('purge'))
                if purgeChild:
                    self._purgeTemplate(child)
                else:
                    self._handleTemplate(child)
            else:
                continue

    def _exportNode(self, node):
        print 'i am _exportNode'

    def _purgeRegistry(self):
        logger = self.environ.getLogger(self._LOGGER_ID)
        registry = self.context
        for template in registry:
            del registry[template]
        logger.info("SiteTemplate registry purged")

    def _purgeTemplate(self, node):
        logger = self.environ.getLogger(self._LOGGER_ID)
        registry = self.context
        tid = node.getAttribute('id')
        registry.remove_template(tid)
        logger.info("Site Template %s purged" % tid)

    def _handleTemplate(self, node):
        logger = self.environ.getLogger(self._LOGGER_ID)
        template_type = node.nodeName.lower()
        handler_name = '_handle_' + template_type
        handler = getattr(self, handler_name, _marker)
        if handler is _marker:
            msg = "Site Template import handler for %s is undefined"
            logger.warning(msg % template_type)
            return
        handler(node)

    def _handle_simpletemplate(self, node):
        logger = self.environ.getLogger(self._LOGGER_ID)
        registry = self.context
        args = []
        for attr in ['id', 'name', 'description']:
            val = node.getAttribute(attr)
            if val == '':
                msg = "Unable to import Site Template, missing value for %s"
                logger.error(msg, attr)
                raise ValueError(msg % attr)
            args.append(val)

        price_val = node.getAttribute('price')
        if price_val == '':
            msg = "Unable to import Site Template, missing value for price"
            logger.error(msg)
            raise ValueError(msg)
        args.append(decimal.Decimal(price_val))

        products = []
        p_nodes = [n for n in node.childNodes if n.nodeName.lower() == 'product']
        for p_node in p_nodes:
            profile = p_node.getAttribute('profile')
            if not self._validateProfile(profile):
                msg = "Unable to import Site Template, bad value for product: %s"
                logger.error(msg, profile)
                raise ValueError(msg % profile)
            products.append(profile)
        args.append(products)

        try:
            template = SimpleSiteTemplate(*args)
        except ValueError, e:
            logger.error(str(e))
            raise e
        else:
            registry.add_template(template)
    
    def _validateProfile(self, profile):
        setup = self.environ.getSetupTool()
        return setup.profileExists(profile)


def importSiteTemplateRegistry(context):
    logger = context.getLogger('eastofeaton.pay2plone')
    registry = queryUtility(ISiteTemplateRegistry, default=_marker)
    if registry is _marker:
        logger.warning("SiteTemplate registry component is missing")
        return

    importer = queryMultiAdapter((registry, context), IBody)
    if importer is None:
        logger.warning("No importer adapter for sitetemplateregistry")
        return

    # set filename on importer so that syntax errors can be reported properly
    try:
        subdir = context._profile_path
    except AttributeError:
        subdir = ''
    path = os.path.join(subdir, importer.name)
    importer.filename = '%s%s' % (path, importer.suffix)
    body = context.readDataFile(importer.filename)
    if body is None:
        return

    importer.body = body
    logger.info("SiteTemplates imported.")


def exportSiteTemplateRegistry(context):
    logger = context.getLogger('eastofeaton.pay2plone')
    registry = queryUtility(ISiteTemplateRegistry, default=_marker)
    if registry is _marker:
        logger.warning('SiteTemplate registry component is missing')
        return
    logger.warning('export of sitetemlate setup is not yet supported')
