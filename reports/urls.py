from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'reports.views.reports_index'),

    
    url(r'^new_report/$', 'reports.views.new_report'),
    url(r'^new_mtr/$', 'pdfgen.views.mtr_generator'),
    url(r'^label/(?P<lot_number>\d+)$', 'pdfgen.report_label.report_label'),
    url(r'^plabel/(?P<lot_number>\d+)$', 'pdfgen.plating_label.plating_label'),
    url(r'^ir/(?P<lot_number>\d+)$', 'pdfgen.blank_inspection_report.blank_inspection_report'),
    url(r'^ir/batch/$', 'pdfgen.blank_inspection_report.batch_inspection_report'),

    url(r'^edit/(?P<lot_number>\d+)$', 'reports.views.edit_report'),
    url(r'^(?P<lot_number>\d+)$', 'reports.views.report'),
)
