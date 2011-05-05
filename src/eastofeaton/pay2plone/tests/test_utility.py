import unittest2 as unittest

from zope.component import queryUtility
from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement
from zope.interface.exceptions import BrokenImplementation
from zope.interface.exceptions import BrokenMethodImplementation

from eastofeaton.pay2plone.interfaces import IPay2PloneUtility
from eastofeaton.pay2plone.interfaces import IPay2PloneUserRecord
# from eastofeaton.pay2plone.sitetemplate import SimpleSiteTemplate
from eastofeaton.pay2plone.utility import Pay2PloneUserRecord

from eastofeaton.pay2plone.testing import\
    EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING


class TestPay2PlayUtility(unittest.TestCase):

    layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.utility = queryUtility(IPay2PloneUtility)

    def test_utility_implements_interface(self):
        """ verify that the utility implements the interface it should
        """
        try:
            self.assertTrue(verifyObject(IPay2PloneUtility, self.utility))
        except DoesNotImplement, e:
            self.fail("Interface not implemented by utility: %s" % str(e))
        except BrokenImplementation, e:
            self.fail("utility is missing a member: %s" % str(e))
        except BrokenMethodImplementation, e:
            msg = "there is a problem with the implementation of a method: %s"
            self.fail(msg % str(e))


class TestPay2PlayUserRecord(unittest.TestCase):

    layer = EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_user_record_implements_interface(self):
        """ verify that the user record object implements its interface
        """
        import pdb; pdb.set_trace( )
        record = Pay2PloneUserRecord()
        try:
            self.assertTrue(verifyObject(IPay2PloneUserRecord, record))
        except DoesNotImplement, e:
            self.fail("Interface not implemented by utility: %s" % str(e))
        except BrokenImplementation, e:
            self.fail("utility is missing a member: %s" % str(e))
        except BrokenMethodImplementation, e:
            msg = "there is a problem with the implementation of a method: %s"
            self.fail(msg % str(e))