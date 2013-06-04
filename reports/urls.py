from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'reports.views.reports_index'),
    
    url(r'^new_report/$', 'reports.views.new_report'),
    url(r'^label/(?P<lot_number>\d+)$', 'reports.views.report_label'),

    url(r'^(?P<lot_number>\d+)$', 'reports.views.report'),
)
