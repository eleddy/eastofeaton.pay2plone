import datetime

from persistent import Persistent
from zope.interface import implements

from eastofeaton.pay2plone.interfaces import ISiteRecord


class SiteRecord(Persistent):
    implements(ISiteRecord)

    def __init__(self, id, template_id):
        self.id = id
        self.template = template_id
        self.purchased = datetime.datetime.utcnow()
        # default term for now is 30 days
        self.term = datetime.timedelta(days=30)
        self.paid = None
        self.created = False
        self.transaction_id = ''
        self.payment_agent = ''

    def mark_paid(self, transaction_id, handler=u'paypal'):
        self.paid = datetime.datetime.utcnow()
        self.transaction_id = transaction_id
        self.payment_agent = handler

    def mark_created(self):
        self.created = True

    def is_expired(self):
        if not self.paid:
            return True
        else:
            expire_date = self.paid + self.term
            return expire_date < datetime.datetime.utcnow()
