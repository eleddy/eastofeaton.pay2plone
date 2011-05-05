from zope.interface import Interface
from zope.container.interfaces import IOrderedContainer
from zope.container.interfaces import IContainerNamesContainer
from zope.container.constraints import contains
from zope.schema import Bool
from zope.schema import TextLine
from zope.schema import Text
from zope.schema import Decimal
from zope.schema import FrozenSet
from zope.schema import Choice
from zope.schema import Datetime
from zope.schema import Timedelta
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


class ISiteRecord(Interface):
    """ describes a record of a site purchase
    """
    id = TextLine(title=u'Site ID')
    template = TextLine(title=u'Template ID used to create this site')
    purchased = Datetime(title=u'Initial purchase date')
    paid = Datetime(title=u'Last payment date')
    transaction_id = TextLine(title=u'Most recent transaction id')
    payment_agent = TextLine(title=u'Payment system used')
    term = Timedelta(title=u'Purchase duration')
    created = Bool(title=u'Site has been created')
    
    def mark_paid():
        """ record datetime.datetime.utcnow as most recent payment datetime
        """

    def mark_created():
        """ record that this site has been created
        """

    def is_expired():
        """ return true if the expiration date for this site has passed
        """


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


class IPay2PloneUtility(IOrderedContainer):
    """ contract interface for the pay2plone utility
    """
    contains("eastofeaton.pay2plone.interfaces.IPay2PloneUserRecord")

    def get_user_record(member_id):
        """ return existing, or create and return new user record for member_id
        """


class IPay2PloneUserRecord(IOrderedContainer, IContainerNamesContainer):
    """ record of sites purchased by a user
    """
    contains("eastofeaton.pay2plone.interfaces.ISiteRecord")

    def add_site_record(site_record):
        """ insert the site_record into the user record, create new id for it
        """

    def get_site_record(id):
        """ return the site record at 'id'
        """

    def delete_site_record(id):
        """ remove the site record at 'id'
        """


class ITemplateListingPage(Interface):
    
    def templates():
        """ provides a list of the templates available in this site
        """