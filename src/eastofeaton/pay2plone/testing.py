from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig


class EastofeatonPay2Plone(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):

        # Load ZCML
        import eastofeaton.pay2plone
        xmlconfig.file('configure.zcml',
                       eastofeaton.pay2plone,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'eastofeaton.pay2plone:default')

EASTOFEATON_PAY2PLONE_FIXTURE = EastofeatonPay2Plone()
EASTOFEATON_PAY2PLONE_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(EASTOFEATON_PAY2PLONE_FIXTURE, ),
                       name="EastofeatonPay2Plone:Integration")
EASTOFEATON_PAY2PLONE_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(EASTOFEATON_PAY2PLONE_FIXTURE, ),
                      name="EastofeatonPay2Plone:Functional")