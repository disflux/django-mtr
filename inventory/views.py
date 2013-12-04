from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from actstream import action

from parts.models import Part
from inventory.models import InventoryLocation, InventoryCount
from inventory.forms import InventoryForm, DirectToPartForm, DirectToLocationForm

def inventory_index(request):
    locations = InventoryLocation.objects.all()
    direct_to_part_form = DirectToPartForm(request.POST)
    direct_to_location_form = DirectToLocationForm(request.POST)
    
    if 'jump' in request.POST:
        jump = request.POST.get('jump', None)
        if jump == 'part':
            part = direct_to_part_form.cleaned_data['jump']
            partobj = Part.objects.get(id=part)
            return HttpResponseRedirect(reverse('inventory.views.part', kwargs={'part_number': partobj.part_number}))
        if jump == 'location':
            if direct_to_location_form.is_valid():
                location = direct_to_location_form.cleaned_data['location']
                return HttpResponseRedirect(reverse('inventory.views.location', kwargs={'location_code': location.location_code}))
    
    return render_to_response('inventory/inventory_index_locations.html',
                              {
                                'locations': locations,
                                'direct_to_location_form': direct_to_location_form,
                                'direct_to_part_form': direct_to_part_form,
                              },
                              context_instance=RequestContext(request))

                              
def new_count(request):
    recent_counts = InventoryCount.objects.all().order_by('-count_timestamp')[:10]
    if request.method == 'POST':
        inventoryform = InventoryForm(request.POST)
        if inventoryform.is_valid():
            part_number = inventoryform.cleaned_data['part'].strip().upper()
            location = inventoryform.cleaned_data['location'].strip().upper()
            count = inventoryform.cleaned_data['inventory_count']
            part = get_object_or_404(Part, part_number=part_number)
            location = get_object_or_404(InventoryLocation, location_code=location)
            inv_count = InventoryCount(part=part, location=location, inventory_count=count, counter=request.user)
            inv_count.save()
            messages.success(request, 'Inventory Count Added')
            return HttpResponseRedirect(reverse('inventory.views.new_count'))
    else:
        inventoryform = InventoryForm()
    return render_to_response('inventory/new_count_bare.html',
                              {
                                'inventoryform': inventoryform,
                                'recent_counts': recent_counts,
                              },
                              context_instance=RequestContext(request))

def location(request, location_code):
    location = InventoryLocation.objects.get(location_code=location_code)
    
    return render_to_response('inventory/location.html',
                              {
                                'location': location,
                              },
                              context_instance=RequestContext(request))

def part(request, part_number):
    pass
    

