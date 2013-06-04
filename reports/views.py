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
from reports.models import Report, ReportDocument

from documents.forms import NewDocumentForm
from documents.models import Document

def reports_index(request):
    reports = Report.objects.all().order_by('-lot_number')
    return render_to_response('reports/reports_index.html',
                              {'reports': reports,
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
            rd = ReportDocument(report=report, document=doc)
            rd.save()
            report.save()
            messages.success(request, 'Document upload successful.')

            return HttpResponseRedirect(reverse('reports.views.report',
                                                    args=[report.lot_number]))
    return render_to_response('reports/report.html', 
                              {
                                  'report': report,
                                  'new_document_form': newdoc,
                              },
                              context_instance=RequestContext(request))


def new_report(request):
    if request.method == 'POST':
        reportform = ReportForm(request.POST)
        if reportform.is_valid():
            report = reportform.save()
            return HttpResponseRedirect(report.get_absolute_url())
    else:
        reportform = ReportForm()
    return render_to_response('reports/new_report.html',
                              {'reportform': reportform,},
                              context_instance=RequestContext(request))





