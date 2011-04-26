from zope.interface import Interface
from zope.container.interfaces import IOrderedContainer
from zope.container.constraints import contains
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
    id = TextLine(title=u'Template ID',
                  description=u'ID must be a valid python identifier',
                  required=True)
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


class ISiteTemplateRegistry(IOrderedContainer):
    """ registry for site templates
    """
    contains("eastofeaton.pay2plone.interfaces.ISiteTemplate")

    def add_template(template):
        """ add a new site template to the template registry
        """

    def remove_template(id):
        """ remove a site template from the template registry
        """

    def list_templates():
        """ return a list of all templates in the template registry
        """

    def get_template_by_id(name):
        """ return the template with name 'name' from the template registry
        """


class IPay2PloneUtility(Interface):
    """ contract interface for the pay2plone utility
    """