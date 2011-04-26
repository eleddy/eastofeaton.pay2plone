import unittest2 as unittest

# from zope.component import queryUtility
# from zope.interface.verify import verifyObject
# from zope.interface.exceptions import DoesNotImplement
# from zope.interface.exceptions import BrokenImplementation
# from zope.interface.exceptions import BrokenMethodImplementation

from eastofeaton.pay2plone.interfaces import ISiteTemplate
from eastofeaton.pay2plone.sitetemplate import SiteTemplate

from eastofeaton.pay2plone.testing import\
    EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING


class TestSiteTemplate(unittest.TestCase):

    layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        template = SiteTemplate('my_template',
                                'Test Template',
                                'This template tests the system',
                                5.00,
                                ['product1', 'product2', 'product3'])
        self.template = template

    def test_provides_interface(self):
        self.assertTrue(ISiteTemplate.providedBy(self.template),
                        'template does not implement ISiteTemplate')