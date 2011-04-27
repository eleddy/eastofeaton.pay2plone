import unittest2 as unittest

# from plone.app.testing import TEST_USER_ID, TEST_USER_PASSWORD
# from plone.app.testing import applyProfile
# from plone.app.testing import setRoles
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility
from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry
from eastofeaton.pay2plone.testing import\
    EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """ validate that our product GS profile has been run and installed
        """
        pid = 'eastofeaton.pay2plone'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        "Package appears not to be installed")

    # def test_utility_available(self):
    #     """ validate that the utility exists and can be found
    #     """
    #     import pdb; pdb.set_trace( )
    #     utility = queryUtility(IPay2PloneUtility)
    #     self.assertTrue(utility is not None)
    
    def test_template_registry_available(self):
        t_registry = queryUtility(ISiteTemplateRegistry, default=None)
        self.assertTrue(t_registry is not None)