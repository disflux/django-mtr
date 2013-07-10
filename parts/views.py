from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from parts.models import Part
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
                              
    

    

