from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Avg, Sum
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from actstream import action

from parts.models import Part
from inventory.models import InventoryLocation, InventoryCount, PartValuation
from inventory.forms import InventoryForm, DirectToPartForm, DirectToLocationForm


def location_ajax(request):
    location = request.GET.get('location', None)
    part = request.GET.get('part')
    part_number = part.strip().upper()
    location_code = location.strip().upper()
    location = InventoryLocation.objects.get(location_code=location_code)
    part = Part.objects.get(part_number=part_number)
    
    count = InventoryCount.objects.filter(part=part, location=location).count()
    if count > 0:
        count_details = InventoryCount.objects.get(part=part, location=location)
    else:
        count_details = None
    
    valuation = PartValuation.objects.get(part=part)
    other_scans = InventoryCount.objects.filter(part=part)
    
    scan = InventoryCount.objects.filter(location=location, part=part)

    return render_to_response('inventory/ajax/location.html',
                              {
                                'count': count,
                                'count_details': count_details,
                                'valuation': valuation,
                                'other_scans': other_scans,
                              },
                              context_instance=RequestContext(request))


    

