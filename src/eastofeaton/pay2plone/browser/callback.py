import decimal

from Products.statusmessages.interfaces import IStatusMessage
from paypal.exceptions import PayPalAPIResponseError

from eastofeaton.pay2plone.browser.base import Pay2PloneBaseView
from eastofeaton.pay2plone.browser.listing import moneyfmt

class PaymentConfirm(Pay2PloneBaseView):

    view_title = "Welcome Back"
    view_description = "Pay2Plone, the easiest way to Plone"
    render_confirmation_form = True

    def _handle_form_submission(self):
        """ handle confirmation of payment
        """
        self.render_confirmation_form = False
        status_messages = IStatusMessage(self.request)
        ## TODO: call do_express_checkout, mark site purchase as complete
        # then redirect to the addsite method at the zope root
        import pdb; pdb.set_trace( )
        if not self.request.get('form.confirm'):
            if self.request.get('form.cancel'):
                # the user cancelled, return to the pay2plone listing page
                view = "/@@pay2plone"
                url = self.context.absolute_url() + view
                self.request.response.redirect(url)
            else:
                # we ended up here in some odd fashion, bug out
                msg = "Unable to complete transaction, invalid user response"
                status_messages.add(msg, type=u'error')
                return self.index()

        # the user positively confirmed, lets do_express_checkout!
        token = self.request.get('form.token')
        payerid = self.request.get('form.payerid')
        amt = self.request.get('form.amt')
        if token is None or payerid is None or amt is None:
            msg = u'Unable to complete transaction, required data not found'
            status_messages.add(msg, type=u'error')
            return self.index()

        api = self.paypal()
        kw = {'payerid': payerid, 'amt': amt, 'paymentaction': 'Sale'}
        try:
            pay_resp = api.do_express_checkout_payment(token, **kw)
        except PayPalAPIResponseError, e:
            msg = u"Error in handling payment: %s" % str(e)
            status_messages.add(msg, type=u'error')
            return self.index()
        
        if pay_resp.paymentstatus.lower() in ['completed', 'processed']:
            # payment good, move on
            pass
        elif pay_resp.paymentstatus.lower() in ['pending']:
            # payment pending, move on with notification to site owner
            pass
        else:
            # payment failed for some reason, report to user
            msg = u'Unable to complete request.  Payment was denied'
            status_messages.add(msg, type='warning')
            
        print 'payment done'

    def _handle_initial_pageload(self):
        ## TODO: call get_express_checkout_details, set up confirmation form
        status_messages = IStatusMessage(self.request)
        token = self.request.get('token', None)
        if token is None:
            self.render_confirmation_form = False
            msg = u"Unable to complete transaction, paypal token not found"
            status_messages.add(msg, type=u"error")
            return self.index()
        self.token = token
        api = self.paypal()
        try:
            get_resp = api.get_express_checkout_details(token)
        except PayPalAPIResponseError, e:
            self.render_confirmation_form = False
            msg = u"Unable to complete transaction: %s" % str(e)
            status_messages.add(msg, type=u'error')
            return self.index()
        
        self.payerid = getattr(get_resp, 'payerid', None)
        self.amt = getattr(get_resp, 'amt', None)
        if self.payerid is None or self.amt is None:
            self.render_confirmation_form = False
            msg = u'Unable to complete transaction: required information not found'
            status_messages.add(msg, type=u'error')
            return self.index()
        
        template_id = get_resp.custom
        template = self.registry.get_template_by_id(template_id)
        if template is None:
            self.render_confirmation_form = False
            msg = u"Unable to complete transaction: no template with id '%s'"
            status_messages.add(msg % template_id, type=u'error')
            return self.index()
        
        if not self._validate_template(get_resp, template):
            self.render_confirmation_form = False
            msg = u"Unable to cemplete transaction: invalid template data"
            status_messages.add(msg, type=u'error')
        
        self.t_dict = {'name': template.name,
                       'id': template.id,
                       'description': template.description,
                       'price_label': moneyfmt(template.price, curr="$")}
        
        return self.index()

    def _validate_template(self, api_response, template):
        return template.price == decimal.Decimal(api_response.amt)


class PaymentCancel(Pay2PloneBaseView):
    
    view_title = "Welcome Back"
    view_description = "Pay2Plone, the easiest way to Plone"

    def _handle_form_submission(self):
        """ handle confirmation of payment
        """
        print 'cancel, already'
        ## TODO: message user about having cancelled, 
        # redirect back to main site root.  We're done.

    def _handle_initial_pageload(self):
        ## TODO: do we need to call paypal api to cancel?
        # provide user with feedback about cancelling, chance to send a
        # message to us?
        pass
