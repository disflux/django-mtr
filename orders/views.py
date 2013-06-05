from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages

from orders.forms import OrderForm, NewLineItemForm
from orders.models import Customer, Order, OrderLineItem
from reports.models import Report


def orders_index(request):
    orders = Order.objects.all()
    
    return render_to_response('orders/orders_index.html',
                              {'orders': orders,},
                              context_instance=RequestContext(request))
    

def order(request, order_number):
    
    order = Order.objects.get(order_number=order_number)
    newli = NewLineItemForm(None)
    
    if 'lineitem_button' in request.POST:
        newli = NewLineItemForm(request.POST)
        if newli.is_valid():
            li = newli.save(commit=False)
            li.order = order
            li.save()
            order.line_items.add(li)
            order.save()
            messages.success(request, 'Report attached')

            return HttpResponseRedirect(reverse('orders.views.order',
                                                    args=[order.order_number]))
    return render_to_response('orders/order.html', 
                              {
                                  'order': order,
                                  'new_lineitem_form': newli,
                              },
                              context_instance=RequestContext(request))
    
def new_order(request):
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            order = orderform.save()
            return HttpResponseRedirect(order.get_absolute_url())
    else:
        orderform = OrderForm()
    return render_to_response('orders/new_order.html',
                              {'orderform': orderform,},
                              context_instance=RequestContext(request))
                              


