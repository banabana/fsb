# -*- mode: python; coding: utf-8; -*-
from livesettings import *
from django.utils.translation import ugettext_lazy as _

PAYMENT_MODULES = config_get('PAYMENT', 'MODULES')
PAYMENT_MODULES.add_choice(('PAYMENT_PREPAID', 'Prepaid Cards'))

PRODUCTS = config_get('PRODUCT', 'PRODUCT_TYPES')
PRODUCTS.add_choice(('prepaid::PrepaidProduct', _('Prepaid Card')))

PAYMENT_GROUP = ConfigurationGroup('PAYMENT_PREPAID', 
    _('Prepaid Card Settings'), 
    requires=PAYMENT_MODULES)

config_register_list(
    BooleanValue(PAYMENT_GROUP, 
        'SSL', 
        description=_("Use SSL for the checkout pages?"), 
        default=False),
        
    StringValue(PAYMENT_GROUP,
        'CHARSET',
        description=_("Character Set"),
        default="BCDFGHKPRSTVWXYZbcdfghkprstvwxyz23456789",
        help_text=_("The characters allowable in randomly-generated certficate codes.  No vowels means no unfortunate words.")),
        
    StringValue(PAYMENT_GROUP,
        'KEY',
        description=_("Module key"),
        hidden=True,
        default = ''),
        
    StringValue(PAYMENT_GROUP,
        'FORMAT',
        description=_('Code format'),
        default="^^^^-^^^^-^^^^",
        help_text=_("Enter the format for your cert code.  Use a '^' for the location of a randomly generated character.")),
        
    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description=_('Implementation module'),
        hidden=True,
        default = 'fsbilling.prepaid'),

    StringValue(PAYMENT_GROUP,
        'LABEL',
        description=_('English name for this group on the checkout screens'),
        default = 'Prepaid Card',
        help_text = _('This will be passed to the translation utility')),
        
    BooleanValue(PAYMENT_GROUP, 
        'LIVE', 
        description=_("Accept real payments"),
        help_text=_("False if you want to be in test mode"),
        default=False),

    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description=_('The url base used for constructing urlpatterns which will use this module'),
        default = r'^prepaid/'),
        
    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description=_("Verbose logs"),
        help_text=_("Add extensive logs during post."),
        default=False)
)
