from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'reports.views.index'),
    
    url(r'^add/$', 'reports.views.addreport'),

    url(r'^(?P<lot_number>\d+)$', 'reports.views.report'),
)
