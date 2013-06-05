from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from documents.models import Document
from orders.models import Order
from parts.models import Part
from reports.models import Report


def home(request):
    documents = Document.objects.all().count()
    reports = Report.objects.all().count()
    orders = Order.objects.all().count()
    parts = Part.objects.all().count()

    return render_to_response('dashboard/home.html', 
                              {
                                  'doc_count': documents,
                                  'report_count': reports,
                                  'order_count': orders,
                                  'part_count': parts,
                              },
                              context_instance=RequestContext(request))
