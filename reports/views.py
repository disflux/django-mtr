from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.core.files.storage import default_storage
from eztables.views import DatatablesView
from reports.forms import ReportForm
from reports.models import Report, ReportDocument

from documents.forms import NewDocumentForm
from documents.models import Document

from orders.models import OrderLineItem

class ReportsDatatablesView(DatatablesView):
    model = Report
    fields = (
        'lot_number',
        'mfg_lot_number',
        'vendor_lot_number',
        'heat_number',
        'vendor__name',
        'part_number__part_number',
        'origin_po',
        'origin_wo',
    )
    template_name = "reports/datatable.html"

def reports_index(request):
    reports = Report.objects.all().order_by('-lot_number')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    paginator = Paginator(reports, 25)

    try:
        reports_list = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        reports_list = paginator.page(1)

            
    return render_to_response('reports/reports_index.html',
                              {'reports': reports_list,
                              },
                              context_instance=RequestContext(request))

def report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number)
    orders = OrderLineItem.objects.filter(report=report)
    newdoc = NewDocumentForm(None)

    if 'document_button' in request.POST:
        newdoc = NewDocumentForm(request.POST, request.FILES)
        if newdoc.is_valid():
            doc = Document(type=newdoc.cleaned_data['type'],
                           file=request.FILES['file'], created_by=request.user)
            doc.save()
            rd = ReportDocument(report=report, document=doc, primary_document=newdoc.cleaned_data['primary'], created_by=request.user, internal_cert=newdoc.cleaned_data['internal'])
            rd.save()
            report.save()
            messages.success(request, 'Document upload successful.')

            return HttpResponseRedirect(reverse('reports.views.report',
                                                    args=[report.lot_number]))
    return render_to_response('reports/report.html', 
                              {
                                  'report': report,
                                  'new_document_form': newdoc,
                                  'orders': orders,
                              },
                              context_instance=RequestContext(request))


def new_report(request):

    if request.method == 'POST':
        reportform = ReportForm(request.POST)
        if reportform.is_valid():
            report = reportform.save()
            report.created_by = request.user
            report.save()
            return HttpResponseRedirect(report.get_absolute_url())
    else:
        copy = request.GET.get('copy', None)
        if copy:
            report = Report.objects.get(lot_number=copy)
            reportform = ReportForm(instance=report)
        else:
            reportform = ReportForm()
    return render_to_response('reports/new_report.html',
                              {'reportform': reportform,},
                              context_instance=RequestContext(request))

def edit_report(request, lot_number):
    report = Report.objects.get(lot_number=lot_number) 
    if request.method == 'POST':
        reportform = ReportForm(request.POST, instance=report)
        if reportform.is_valid():
            report = reportform.save()
            
            return HttpResponseRedirect(report.get_absolute_url())
    else:
        reportform = ReportForm(instance=report)
    return render_to_response('reports/new_report.html',
                              {'reportform': reportform,},
                              context_instance=RequestContext(request))
                              





