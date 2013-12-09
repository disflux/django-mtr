from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'inventory.views.inventory_index'),
    url(r'^new_count/$', 'inventory.views.new_count'),
    url(r'^part/(?P<part_number>\.+)$', 'inventory.views.part'),
    url(r'^audit/(?P<scan_id>\d+)$', 'inventory.views.switch_audit'),
    url(r'^location_labels/$', 'pdfgen.location_labels.location_labels'),
    url(r'^location/(?P<location_code>.+)$', 'inventory.views.location'),

)
