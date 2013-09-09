from collections import defaultdict
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from documents.models import Document
from orders.models import Order
from parts.models import Part
from reports.models import Report
from dashboard.models import NewsItem

from actstream import action
from actstream.models import model_stream

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
    report_graph = defaultdict(int)
    for r in data:
        report_graph[r.created_at.strftime("%Y%m%d")] += 1
    r_graph = []
    for k, v in report_graph.iteritems():
        r_graph.append(v)
    
    data = Document.objects.filter(created_at__gte=date)
    dv = defaultdict(int)
    for r in data:
        dv[r.created_at.strftime("%Y%m%d")] += 1
    d_graph = []
    for k, v in dv.iteritems():
        d_graph.append(v)
    
    data = Order.objects.filter(created_at__gte=date)
    dv = defaultdict(int)
    for r in data:
        dv[r.created_at.strftime("%Y%m%d")] += 1
    o_graph = []
    for k, v in dv.iteritems():
        o_graph.append(v)
    
    data = Part.objects.filter(created_at__gte=date)
    dv = defaultdict(int)
    for r in data:
        dv[r.created_at.strftime("%Y%m%d")] += 1
    p_graph = []
    for k, v in dv.iteritems():
        p_graph.append(v)
        

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
