from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from vendors.models import Vendor
from reports.models import Report

def vendors_index(request):
    vendors = Vendor.objects.all()
    
    return render_to_response('vendors/vendors_index.html',
                              {'vendors': vendors,
                              },
                              context_instance=RequestContext(request))

def vendor(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    reports = Report.objects.filter(vendor=vendor)

    return render_to_response('vendors/vendor.html',
                              {'vendor': vendor,
                               'reports': reports,
                              },
                              context_instance=RequestContext(request))
