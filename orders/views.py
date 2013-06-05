from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages

from orders.forms import OrderForm
from orders.models import Customer, Order, OrderLineItem


def orders_index(request):
    pass

def order(request):
    pass
    
def new_order(request):
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            order = reportform.save()
            return HttpResponseRedirect(order.get_absolute_url())
    else:
        orderform = OrderForm()
    return render_to_response('orders/new_order.html',
                              {'orderform': orderform,},
                              context_instance=RequestContext(request))

