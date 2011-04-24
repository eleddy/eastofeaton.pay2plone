from zope.interface import Interface
from zope.schema import TextLine
from zope.schema import Text
from zope.schema import Decimal
from zope.schema import FrozenSet
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ISiteTemplate(Interface):
    """ describes the template for creating a site
    """
    name = TextLine(title=u'Template Name',
                    required=True)
    description = Text(title=u"Template Description",
                       description=u"The description of this template shown to users",
                       required=True)
    price = Decimal(title=u"Template Price",
                    description=u"The price users will be charged per subscription period for a site built from this template",
                    required=True)
    products = FrozenSet(title=u"Installed Products",
                         description=u"Choose the products to install when creating a site from this template",
                         required=True,
                         value_type=Choice(
                            vocabulary=SimpleVocabulary((
                                SimpleTerm(token='Foo', value='foo'),
                                SimpleTerm(token='Bar', value='bar'),
                                SimpleTerm(token='Baz', value='baz'),
                            )),
                         ),
                         default=frozenset(['foo',]))


class IPay2PloneUtility(Interface):
    """ contract interface for the pay2plone utility
    """
