from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'parts.views.parts_index', name='parts_index'),
    url(r'^new_part/$', 'parts.views.new_part'),
    url(r'^label/$', 'parts.views.part_label'),
    url(r'^show_label/(?P<part_number>.+)/$', 'pdfgen.part_label.part_label'),
    url(r'^edit/(?P<part_number>.+)/$', 'parts.views.edit_part'),    
    url(r'^(?P<part_number>.+)/$', 'parts.views.part'),
    
    
)
