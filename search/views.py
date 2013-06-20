from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from reports.models import Report
from search.forms import SearchForm

import re

def index(request):
    return render_to_response('search/search.html',
                              {},
                              context_instance=RequestContext(request))

def results(request):
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
                suggestions = sqs.spelling_suggestion()
                results = sqs.filter(content=AutoQuery(q))

        else:
            results = []

    return render_to_response('search/search.html',
                              { 
                                  'results_list': results, 
                                  'query': q,
                                 # 'facets': results.facet_counts(),
                              },
                              context_instance=RequestContext(request))