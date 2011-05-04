from decimal import Decimal

from Products.statusmessages.interfaces import IStatusMessage

from eastofeaton.pay2plone.browser.base import Pay2PloneBaseView


# reference:  http://docs.python.org/release/2.6.6/library/decimal.html#recipes

def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


class TemplateListings(Pay2PloneBaseView):

    view_title = "Pay-2-Plone"
    view_description = "The easiest way to Plone"
    payment_return_view = '/@@pay2plone_confirm'
    payment_cancel_view = '/@@pay2plone_cancel'
    buy_button_name = 'buypaypal'

    def __init__(self, context, request):
        super(TemplateListings, self).__init__(context, request)
        base_url = self.context.absolute_url()
        self.return_url = base_url + self.payment_return_view
        self.cancel_url = base_url + self.payment_cancel_view

    def templates(self):
        tids = self.registry.list_templates()
        templates = []
        for tid in tids:
            template = self.registry.get_template_by_id(tid)
            if template is not None:
                t_dict = {'name': template.name,
                          'id': template.id,
                          'description': template.description,
                          'price_label': moneyfmt(template.price, curr="$")}
                templates.append(t_dict)
        return templates

    def _handle_form_submission(self):
        form = self.request.form
        template_id = form.get(self.buy_button_name, None)
        if template_id is not None:
            # we've  chosen to buy a site, get it
            template = self.registry.get_template_by_id(template_id)
            if template is not None:
                # base_kw_string = 'paymentrequest_0_'
                kw = {'reqconfirmshipping': 0,
                      'noshipping': 1,
                      'returnurl': self.return_url,
                      'cancelurl': self.cancel_url,
                      'paymentaction': 'Order'}
                for kw_str, templ_attr in [('amt', 'price'),
                                           ('itememt', 'price'),
                                           ('desc', 'description'),
                                           ('custom', 'id')]:
                    # keyword = base_kw_string + kw_str
                    value = getattr(template, templ_attr, None)
                    kw[kw_str] = value
                    # kw[keyword] = '%s' % value
                    # if kw_str == 'amt':
                        # kw[kw_str] = '%s' % value
                api = self.paypal()
                set_ec_resp = api.set_express_checkout(**kw)
                if not set_ec_resp or not set_ec_resp.success:
                    msg = "We've had a problem reaching paypal, please try "
                    msg += "again later."
                    IStatusMessage(self.request).add(msg, type=u'error')
                    return self.index()
                token = set_ec_resp.token
                pp_url = api.generate_express_checkout_redirect_url(token)
                ## TODO: use p2p_utility to set up provisional site purchase
                self.request.response.redirect(pp_url)
