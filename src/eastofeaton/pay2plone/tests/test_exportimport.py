import unittest2 as unittest
import decimal

from zope.component import getMultiAdapter

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.testing import BodyAdapterTestCase
from Products.GenericSetup.testing import DummySetupEnviron

from eastofeaton.pay2plone.sitetemplate import SimpleSiteTemplate
from eastofeaton.pay2plone.registry import SiteTemplateRegistry
from eastofeaton.pay2plone.testing import Pay2PloneZCMLLayer


_SIMPLE_SITE_TEMPLATE_XML = """\
<?xml version="1.0"?>
<object>
 <simpletemplate id="foo" 
                 name="I am the foo template" 
                 description="this is my description"
                 price="5.00"
                 >
  <product profile="eastofeaton.pay2plone:default" />
 </simpletemplate>
</object>
"""


class DummySetupTool(object):
    
    def __init__(self, profile_exists_value):
        self._profile_exists = profile_exists_value

    def profileExists(self, profile):
        return self._profile_exists


class Pay2PloneDummySetupEnviron(DummySetupEnviron):
    
    def __init__(self, profile_exists_value):
        self._notes = []
        self._should_purge = True
        self._setup_tool = DummySetupTool(profile_exists_value)

    def getSetupTool(self):
        return self._setup_tool


class TestSiteTemplateRegsitryAdapter(BodyAdapterTestCase, unittest.TestCase):

    layer = Pay2PloneZCMLLayer
    # layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING
    
    def _getTargetClass(self):
        from eastofeaton.pay2plone.exportimport.registry import \
            SiteTemplateRegistryXMLAdapter
        return SiteTemplateRegistryXMLAdapter

    def setUp(self):
        self._obj = SiteTemplateRegistry()
        self._BODY = _SIMPLE_SITE_TEMPLATE_XML
    
    def test_body_get(self):
        self._populate(self._obj)
        context = Pay2PloneDummySetupEnviron(True)
        self.fail("export of site templates is not yet implemented")
        context
        # adapted = getMultiAdapter((self._obj, context), IBody)
        # self.assertEqual(adapted.body, self._BODY)

    def test_body_set(self):
        context = Pay2PloneDummySetupEnviron(True)
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        self._verifyImport(self._obj)
        # following tests re-export, which is not yet implemented, skip for now
        # self.assertEqual(adapted.body, self._BODY)

        # now in update mode
        context._should_purge = False
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        # following tests re-export, which is not yet implemented, skip for now
        # self.assertEqual(adapted.body, self._BODY)

        # and again in update mode
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        # following tests re-export, which is not yet implemented, skip for now
        # self.assertEqual(adapted.body, self._BODY)

    def _verifyImport(self, obj):
        import pdb; pdb.set_trace( )
        t_list = obj.list_templates()
        self.assertEqual(len(t_list), 1)
        self.assertTrue(u'foo' in t_list)
        template = obj.get_template_by_id(u'foo')
        self.assertTrue(isinstance(template, SimpleSiteTemplate))
        self.assertEquals(template.id, u'foo')
        self.assertEquals(template.name, u'I am the foo template')
        self.assertEquals(template.description, u'this is my description')
        self.assertEquals(template.price, decimal.Decimal('5.00'))
        self.assertEquals(len(template.products), 1)
        self.assertTrue('eastofeaton.pay2plone:default' in template.products)
