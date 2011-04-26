import unittest2 as unittest

from zope.component import queryUtility
from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement
from zope.interface.exceptions import BrokenImplementation
from zope.interface.exceptions import BrokenMethodImplementation
from zope.container.interfaces import InvalidItemType

from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry
from eastofeaton.pay2plone.interfaces import ISiteTemplate
from eastofeaton.pay2plone.sitetemplate import SimpleSiteTemplate

from eastofeaton.pay2plone.testing import\
    EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING


class FakeTemplate(object):

    def __init__(self):
        self.id = 'foo'
        self.name= 'foobar'
        self.description = 'a non-template template'
        self.price = 5.00
        self.products = ['a', 'b', 'c']


class TestSiteTemplateRegistry(unittest.TestCase):

    layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.registry = queryUtility(ISiteTemplateRegistry)

    def insert_template(self):
        """ insert a template into the registry through the backdoor
            use the container api to do it.
        """
        sample_template = SimpleSiteTemplate(
            'sampleid',
            'My Name',
            'A test template',
            10.00,
            ['productA', 'productB', 'productC'])
        self.registry['sampleid'] = sample_template

    def test_registry_interface(self):
        try:
            self.assertTrue(verifyObject(ISiteTemplateRegistry, self.registry))
        except DoesNotImplement, e:
            self.fail("Interface not implemented by utility: %s" % str(e))
        except BrokenImplementation, e:
            self.fail("utility is missing a member: %s" % str(e))
        except BrokenMethodImplementation, e:
            msg = "there is a problem with the implementation of a method: %s"
            self.fail(msg % str(e))

    def test_add_template(self):
        """ verify that we can add a template to the utility and get it back
        """
        test_template = SimpleSiteTemplate(
            'myid',
            'My Name',
            'A test template',
            5.00,
            ['produc1', 'product2', 'product3'])
        # there should be no templates in the registry now:
        self.assertEquals(len(self.registry), 0,
                          "unexpected template present in registry")
        # add one
        self.registry.add_template(test_template)
        t_list = self.registry.keys()
        self.assertEquals(len(t_list), 1,
                          "template should be registered, but is not")
        self.assertEquals(t_list[0], 'myid',
                          "template registered with wrong id: %s" % t_list[0])

    def test_add_non_template(self):
        """ verify that adding a non-template object raises an error
        """
        test_template = FakeTemplate()
        self.assertRaises(InvalidItemType, 
                          self.registry.add_template,
                          test_template)

    def test_remove_template(self):
        # set us up with a single template by the id 'sampleid'
        self.insert_template()
        self.assertEquals(len(self.registry), 1,
                          'we appear not to have a registered template')
        # attempting to remove a non-existant template should not be a problem
        try:
            self.registry.remove_template('myid')
        except Exception, e:
            msg = "attempt to remove non-existent template raised an error %s"
            self.fail(msg % str(e))
        self.registry.remove_template('sampleid')
        self.assertEquals(len(self.registry), 0,
                          'a template remains in the registry')

    def test_list_templates(self):
        # insert a single template with the id 'sampleid'
        self.insert_template()
        t_list = self.registry.list_templates()
        self.assertEquals(len(t_list), 1,
                          'expected 1 template, got %s' % len(t_list))
        self.assertTrue('sampleid' in t_list,
                        "'sampleid' not found in template list: %s" % t_list)

    def test_get_template_by_id(self):
        # insert a single template with the id 'sampleid'
        self.insert_template()
        my_template = self.registry.get_template_by_id('sampleid')
        self.assertTrue(ISiteTemplate.providedBy(my_template))
        self.assertEquals(my_template.name, "My Name")
        self.assertEquals(len(my_template.products), 3,
                          "template should have three products listed")
