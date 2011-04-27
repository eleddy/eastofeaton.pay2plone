from persistent import Persistent

from zope.interface import implements

from eastofeaton.pay2plone.interfaces import ISiteTemplate


class SimpleSiteTemplate(Persistent):
    """ a template for a purchaseable site
    """
    implements(ISiteTemplate)

    id = u''
    name = u''
    description = None
    template_price = 0.0
    products = None

    def __init__(self, id, name, description, price, products=[]):
        try:
            class test(object): __slots__ = [id]
        except TypeError:
            raise ValueError('id must be a valid python identifier')
        else:
            self.id = id
        self.name = name
        self.description = description
        self.template_price = price
        self.products = frozenset(products)

    @property
    def price(self):
        return self.template_price
