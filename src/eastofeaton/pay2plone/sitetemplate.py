from persistent import Persistent

from zope.interface import implements

from eastofeaton.pay2plone.interfaces import ISiteTemplate


class SiteTemplate(Persistent):
    """ a template for a purchaseable site
    """
    implements(ISiteTemplate)
    
    name = u''
    description = None
    price = 0.0
    products = None
    
    def __init__(self, name, description, price, products=[]):
        self.name = name
        self.description = description
        self.price = price
        self.products = frozenset(products)