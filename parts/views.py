from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from actstream import action

from parts.models import Part
from parts.forms import NewPartForm
from reports.models import Report

def parts_index(request):
    parts = Part.objects.all()
    
    return render_to_response('parts/parts_index.html',
                              {'parts': parts,
                              },
                              context_instance=RequestContext(request))

def part(request, part_number):
    part = Part.objects.get(part_number=part_number)
    reports = Report.objects.filter(part_number=part)
    return render_to_response('parts/part.html',
                              {'part': part,
                               'reports': reports,
                              },
                              context_instance=RequestContext(request))
                              
def new_part(request):
    if request.method == 'POST':
        partform = NewPartForm(request.POST)
        if partform.is_valid():
            part = partform.save()
            part.created_by = request.user
            part.save()
            action.send(request.user, verb="created part", target=part)
            return HttpResponseRedirect(part.get_absolute_url())
    else:
        partform = NewPartForm()
    return render_to_response('parts/new_part.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))
                              
def edit_part(request, part_number):
    p = Part.objects.get(part_number=part_number)
    if request.method == 'POST':
        partform = NewPartForm(request.POST, instance=p)
        if partform.is_valid():
            part = partform.save()
            part.created_by = request.user
            part.save()
            action.send(request.user, verb="edited part", target=part)
            return HttpResponseRedirect(part.get_absolute_url())
    else:
        partform = NewPartForm(instance=p)
    return render_to_response('parts/new_part.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))
                              
    

    

