from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'^$', include('haystack.urls')),
    #url(r'^advanced/$', 'search.views.index'),
    #url(r'^autocomplete/$', 'search.autocomplete.autocomplete'),
    url(r'^$', 'search.views.results', name='search'),
)
