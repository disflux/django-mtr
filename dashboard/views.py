from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from documents.models import Document
from orders.models import Order
from parts.models import Part
from reports.models import Report
from dashboard.models import NewsItem

from actstream import action
from actstream.models import model_stream
from mtr import graph_utils

import datetime


def home(request):
    date = datetime.datetime.today() - datetime.timedelta(days=30)
    documents = Document.objects.all().count()
    reports = Report.objects.all().count()
    orders = Order.objects.all().count()
    parts = Part.objects.all().count()
    log = model_stream(request.user)[:8]
    news = NewsItem.objects.all().order_by('-date')[:5]
    
    data = Report.objects.filter(created_at__gte=date)
    r_graph = graph_utils.flot_values(data)
    
    data = Document.objects.filter(created_at__gte=date)
    d_graph = graph_utils.flot_values(data)
    
    data = Order.objects.filter(created_at__gte=date)
    o_graph = graph_utils.flot_values(data)
    
    data = Part.objects.filter(created_at__gte=date)
    p_graph = graph_utils.flot_values(data)
    
    return render_to_response('dashboard/home.html', 
                              {
                                  'doc_count': documents,
                                  'report_count': reports,
                                  'order_count': orders,
                                  'part_count': parts,
                                  'log': log,
                                  'news': news,
                                  'report_graph': r_graph,
                                  'document_graph': d_graph,
                                  'order_graph': o_graph,
                                  'part_graph': p_graph,
                              },
                              context_instance=RequestContext(request))
