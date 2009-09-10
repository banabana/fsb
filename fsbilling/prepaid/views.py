# -*- mode: python; coding: utf-8; -*-
from django import http
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from forms import PrepaidCodeForm, PrepaidPayShipForm
from models import Prepaid, PREPAIDCODE_KEY
from livesettings import config_get_group
from satchmo_store.shop.models import Order
from payment.utils import pay_ship_save, get_or_create_order
from payment.views import confirm, payship
from satchmo_utils.dynamic import lookup_url
from django.contrib.sites.models import Site
import logging

log = logging.getLogger("prepaid.views")

gc = config_get_group('PAYMENT_PREPAID')
    
def prepaidcert_pay_ship_process_form(request, contact, working_cart, payment_module):
    if request.method == "POST":
        new_data = request.POST.copy()
        form = PrepaidPayShipForm(request, payment_module, new_data)
        if form.is_valid():
            data = form.cleaned_data

            # Create a new order.
            newOrder = get_or_create_order(request, working_cart, contact, data)            
            newOrder.add_variable(PREPAIDCODE_KEY, data['prepaidcode'])
            
            request.session['orderID'] = newOrder.id

            url = None
            if not url:
                url = lookup_url(payment_module, 'satchmo_checkout-step3')
                
            return (True, http.HttpResponseRedirect(url))
    else:
        form = PrepaidPayShipForm(request, payment_module)

    return (False, form)

    
def pay_ship_info(request):
    return payship.base_pay_ship_info(request, 
        gc, 
        prepaidcert_pay_ship_process_form,
        template="shop/checkout/prepaid/pay_ship.html")
    
def confirm_info(request, template="shop/checkout/prepaid/confirm.html"):
    try:
        order = Order.objects.get(id=request.session['orderID'])
        prepaidcert = Prepaid.objects.from_order(order)
    except (Order.DoesNotExist, Prepaid.DoesNotExist, KeyError):
        prepaidcert = None
           
    controller = confirm.ConfirmController(request, gc)
    controller.templates['CONFIRM'] = template
    controller.extra_context={'prepaidcert' : prepaidcert}
    controller.confirm()
    return controller.response

def check_balance(request):
    if request.method == "GET":        
        code = request.GET.get('code', '')
        if code:
            try:
                gc = Prepaid.objects.get(code=code, 
                    value=True, 
                    site=Site.objects.get_current())
                success = True
                balance = gc.balance
            except Prepaid.DoesNotExist:
                success = False
        else:
            success = False
        
        ctx = RequestContext(request, {
            'code' : code,
            'success' : success,
            'balance' : balance,
            'prepaid' : gc
        })
    else:
        form = PrepaidCodeForm()
        ctx = RequestContext(request, {
            'code' : '',
            'form' : form
        })
    return render_to_response(ctx, 'prepaid/balance.html')
