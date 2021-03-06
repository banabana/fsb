# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management import call_command

class Command(NoArgsCommand):
    help = "Load FSbilling default data."
    
    def handle_noargs(self, **options):
        """Load FSadmin default data."""
        call_command('loaddata', 'currency_base.xml', 'currency.xml', 'tariffplan.xml', 'l10n-data.yaml', 'product_category', 'product', 'prepaid', interactive=True)
