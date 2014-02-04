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


def dashboard(request):
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
                
    part_numbers = Part.objects.all().count()
    parts_with_stock = PartValuation.objects.filter(quantity__gt=0).count()
    valuation = PartValuation.objects.all().aggregate(valuation=Sum('ext_value'))
    raw_lbs = PartValuation.objects.filter(uom='LB').aggregate(lbs=Sum('quantity'))
    pcs = PartValuation.objects.filter(uom='EA').aggregate(pcs=Sum('quantity'))
    total_pcs = PartValuation.objects.all().aggregate(total_pcs=Sum('quantity'))
    
    avg_cost = valuation['valuation'] / total_pcs['total_pcs']
    
    bin_locations = InventoryLocation.objects.all().count()

    scans = InventoryCount.objects.all().count()
    scan_times = InventoryCount.objects.all().aggregate(scans=Sum('scans'))
    #scan_locations = InventoryCount.objects.order_by('location').distinct('location')
    
    scanned = InventoryCount.objects.all()
    uniques = []
    for s in scanned:
        if s.part not in uniques:
            uniques.append(s.part)
    pre_value = 0
    reserve_value = 0
    skipped = 0
    for s in uniques:
        try:
            value_obj = PartValuation.objects.get(part=s)
            pre_value += value_obj.ext_value
            reserve_value += value_obj.applied_quantity * value_obj.stocking_cost
        except:
            skipped += 1

    
    post_value = InventoryCount.objects.all().aggregate(post_value=Sum('stocking_value'))
    
    dollar_difference = float(post_value['post_value']) - float(pre_value)
    percent_difference = (1.0 - (float(post_value['post_value']) / float(pre_value))) * 100
    
    reserve_difference = float(dollar_difference) - float(reserve_value)
        

    return render_to_response('inventory/dashboard.html',
                              {
                                  'part_numbers': part_numbers,
                                  'part_stock': parts_with_stock,
                                  'scans': scans,
                                  'valuation': valuation,
                                  'raw_lbs': raw_lbs,
                                  'pcs': pcs,
                                  'avg_cost': avg_cost,
                                  'direct_to_location_form': direct_to_location_form,
                                  'direct_to_part_form': direct_to_part_form,
                                  'bin_locations': bin_locations,
                                  'scan_times': scan_times,
                                  'pre_value': pre_value,
                                  'post_value': post_value['post_value'],
                                  'reserve_value': reserve_value,
                                  'skipped': skipped,
                                  'dollar_difference': dollar_difference,
                                  'percent_difference': percent_difference,
                                  'reserve_difference': reserve_difference,
                              },
                              context_instance=RequestContext(request))

def inventory_index(request):
    locations = InventoryLocation.objects.filter(inventorycount__audited=False).order_by('location_code').distinct()
    direct_to_part_form = DirectToPartForm(request.POST)
    direct_to_location_form = DirectToLocationForm(request.POST)
    
    if 'jump' in request.POST:
        jump = request.POST.get('jump', None)
        if jump == 'part':
            if direct_to_part_form.is_valid():
                part = direct_to_part_form.cleaned_data['part']
                return HttpResponseRedirect(reverse('inventory.views.part_inv', kwargs={'part_number': part.part_number}))
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
                              
def inventory_index_parts(request):
    parts = InventoryCount.objects.all().order_by('part')
    scanned = InventoryCount.objects.all()
    uniques = []
    unique_counts = []
    for s in scanned:
        if s.part not in uniques:
            uniques.append(s.part)
            unique_counts.append(s)

    direct_to_part_form = DirectToPartForm(request.POST)
    direct_to_location_form = DirectToLocationForm(request.POST)
    
    
    if 'jump' in request.POST:
        jump = request.POST.get('jump', None)
        if jump == 'part':
            if direct_to_part_form.is_valid():
                part = direct_to_part_form.cleaned_data['part']
                return HttpResponseRedirect(reverse('inventory.views.part_inv', kwargs={'part_number': part.part_number}))
        if jump == 'location':
            if direct_to_location_form.is_valid():
                location = direct_to_location_form.cleaned_data['location']
                return HttpResponseRedirect(reverse('inventory.views.location', kwargs={'location_code': location.location_code}))
    
    return render_to_response('inventory/inventory_index_parts.html',
                              {
                                'parts': unique_counts,
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
            complete = inventoryform.cleaned_data['location_complete']
            part = get_object_or_404(Part, part_number=part_number)
            location = get_object_or_404(InventoryLocation, location_code=location)
            inv_count, _created = InventoryCount.objects.get_or_create(part=part, location=location)
            if _created:
                inv_count.inventory_count = count
                inv_count.scans = 1
            else:
                inv_count.inventory_count += count
                inv_count.scans += 1
            inv_count.counter = request.user
            inv_count.count_complete=complete
            inv_count.save()
            messages.success(request, 'Inventory Count Added')
            return HttpResponseRedirect(reverse('inventory.views.new_count'))
    else:
        inventoryform = InventoryForm()
    return render_to_response('inventory/new_count.html',
                              {
                                'inventoryform': inventoryform,
                                'recent_counts': recent_counts,
                              },
                              context_instance=RequestContext(request))

def location(request, location_code):
    location = InventoryLocation.objects.get(location_code=location_code)
    total_part_numbers = InventoryCount.objects.filter(location=location).count()
    agg = InventoryCount.objects.filter(location=location).aggregate(stocking_value=Sum('stocking_value'), total_parts=Sum('inventory_count'))
        
    
    return render_to_response('inventory/location.html',
                              {
                                  'location': location,
                                  'total_part_numbers': total_part_numbers,
                                  'agg': agg,

                              },
                              context_instance=RequestContext(request))
                              
def part_inv(request, part_number):
    part = Part.objects.get(part_number=part_number)
    
    scans = InventoryCount.objects.filter(part=part)
    agg = InventoryCount.objects.filter(part=part).aggregate(scans=Sum('scans'), total_parts=Sum('inventory_count'))    
    
    return render_to_response('inventory/part.html',
                              {
                                  'part': part,
                                  'scans': scans,
                                  'agg': agg,
                              },
                              context_instance=RequestContext(request))

def switch_audit(request, scan_id):
    scan = InventoryCount.objects.get(pk=scan_id)
    if 'part' in request.GET:
        part = 1
    else:
        part = None
    if scan.audited == True:
        scan.audited = False
        scan.auditor = None
    else:
        scan.audited = True
        scan.auditor = request.user
    scan.save()

    #if request.is_ajax():
    return render_to_response('inventory/scan_row.html',
                                  {
                                      'scan': scan,
                                      'part': part,
                                  },
                                  context_instance=RequestContext(request))
    #else:
    #    return HttpResponseRedirect(reverse('inventory.views.location', kwargs={'location_code': scan.location.location_code}))

def part(request, part_number):
    pass
    

