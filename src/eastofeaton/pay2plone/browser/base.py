from zope.publisher.browser import BrowserView
from zope.component import queryUtility
from Products.statusmessages.interfaces import IStatusMessage
from eastofeaton.paypal.interfaces import IPaypalAPIUtility

from eastofeaton.pay2plone.interfaces import ISiteTemplateRegistry
from eastofeaton.pay2plone.interfaces import IPay2PloneUtility


_marker = object()


class Pay2PloneBaseView(BrowserView):
    """ base view class for pay2plone views

        common functionality goes here:
            set template_registry, paypal utility and pay2plone utility
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.registry = queryUtility(ISiteTemplateRegistry, default=_marker)
        self.p2p_utility = queryUtility(IPay2PloneUtility, default=_marker)
        self.paypal = queryUtility(IPaypalAPIUtility, default=_marker)

    def __call__(self):
        """ handle form if submitted, otherwise render page
        """
        if not self._check_api_tools():
            return self.index()
        form = self.request.form
        submitted = form.get('form.submitted', False)
        if submitted:
            return self._handle_form_submission()
        else:
            return self._handle_initial_pageload()

    def _check_api_tools(self):
        """ verify that required api tools are present
        """
        if self.registry is _marker or \
            self.paypal is _marker or \
            self.p2p_utility is _marker:
            # we've got a problem, message the user and return the page
            msg = "Unable to proceed, cannot locate required configuration. "
            msg += "Please notify site administration of this problem."
            IStatusMessage(self.request).add(msg, type=u'error')
            return False
        return True

    def _handle_form_submission(self):
        """ subclasses are responsible for implementing this
        """
        raise NotImplementedError()

    def _handle_initial_pageload(self):
        """ subclasses may override this if additional steps are needed
        """
        return self.index()
