from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify, truncatechars
from django.db import IntegrityError
from django.db.models import Avg, Max, Min
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.files.storage import default_storage

from reports.forms import ReportForm
from reports.models import Report

from documents.forms import NewDocumentForm
from documents.models import Document

def index(request):
    return render_to_response('parts/index.html',
                              {'parts_list': parts_list,
                               'page_num': page,
                              },
                              context_instance=RequestContext(request))

def report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)
    newdoc = NewDocumentForm(None)

    if 'document_button' in request.POST:
        newdoc = NewDocumentForm(request.POST, request.FILES)
        if newdoc.is_valid():
            doc = Document(type=newdoc.cleaned_data['type'],
                           file=request.FILES['file'])
            doc.save()
            report.documents.add(doc)
            report.save()
            messages.success(request, 'Document upload successful. Thanks for contributing!')

            return HttpResponseRedirect(reverse('reports.views.report',
                                                    args=[report.lot_number]))
    return render_to_response('reports/report.html', 
                              {
                                  'report': report,
                                  'new_document_form': newdoc,
                              },
                              context_instance=RequestContext(request))

def addpart(request, part_number, company, desc):
    try:
        c = Company.objects.get(slug=slugify(company))
    except ObjectDoesNotExist:
        c = Company(name=company, slug=slugify(company))
        c.save()
    if Part.objects.filter(number=part_number, company=c).exists():
        newpart = Part.objects.get(number=part_number, company=c)
    else: 
        newpart = Part(number=part_number, company=c, user=request.user, description=desc, hits=0)
        newpart.save()
    return newpart

def addreport(request):
    if request.method == 'POST':
        reportform = XrefForm(request.POST)
        if partform.is_valid():
            part_number = partform.cleaned_data['part'].upper()
            desc = partform.cleaned_data['desc'].upper()
            company = partform.cleaned_data['company'].upper()
            newpart = addpart(request, part_number, company, desc)
            return HttpResponseRedirect(newpart.get_absolute_url())
    else:
        partform = XrefForm()
    return render_to_response('parts/add.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))





