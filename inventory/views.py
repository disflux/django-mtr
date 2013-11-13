from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from actstream import action

from parts.models import Part
from inventory.models import InventoryLocation, InventoryCount
from inventory.forms import InventoryForm

def inventory_index(request):
    locations = InventoryLocation.objects.all()
    
    return render_to_response('inventory/inventory_index_locations.html',
                              {'locations': locations,
                              },
                              context_instance=RequestContext(request))

                              
def new_count(request):
    if request.method == 'POST':
        inventoryform = InventoryForm(request.POST)
        if inventoryform.is_valid():
            inventoryform.save()
            messages.success(request, 'Inventory Count Added')
            return HttpResponseRedirect(reverse('inventory.views.new_count'))
    else:
        inventoryform = InventoryForm()
    return render_to_response('inventory/new_count.html',
                              {'inventoryform': inventoryform,},
                              context_instance=RequestContext(request))

