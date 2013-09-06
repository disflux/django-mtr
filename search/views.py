import time
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from reports.models import Report
from search.forms import SearchForm

def index(request):
    return render_to_response('search/search.html',
                              {},
                              context_instance=RequestContext(request))

def results(request):
    start = time.time()
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return render_to_response('search/search.html', context_instance=RequestContext(request))
    
    if searchform.is_valid():
        q = searchform.cleaned_data['q']

        if q:
            try:
                report = Report.objects.get(lot_number=q)
                return redirect('reports.views.report', lot_number=report.lot_number)
            except:
                sqs = SearchQuerySet().auto_query(q)
                results = sqs.filter(content=AutoQuery(q))

        else:
            results = []
        
        try:                                                                    
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(sqs, 20, request=request)
        results_list = p.page(page)

        end = time.time()
        
        runtime = end-start

    return render_to_response('search/search.html',
                              { 
                                  'results_list': results_list, 
                                  'query': q,
                                  'runtime': runtime,
                              },
                              context_instance=RequestContext(request))