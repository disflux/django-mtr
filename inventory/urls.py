from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'inventory.views.dashboard'),
    url(r'^locations', 'inventory.views.inventory_index'),
    url(r'^parts', 'inventory.views.inventory_index_parts'),
    url(r'^new_count/$', 'inventory.views.new_count'),
    url(r'^part/(?P<part_number>\.+)$', 'inventory.views.part'),
    url(r'^audit/(?P<scan_id>\d+)$', 'inventory.views.switch_audit'),
    url(r'^location_labels/$', 'pdfgen.location_labels.location_labels'),
    url(r'^location_scan_sheet/$', 'pdfgen.location_scan_sheet.location_scan_sheet'),
    url(r'^location/(?P<location_code>.+)$', 'inventory.views.location'),
    url(r'^part/(?P<part_number>.+)$', 'inventory.views.part_inv'),
    url(r'^scansexport/$', 'inventory.views.export_scans'),
    url(r'^deletescans/$', 'inventory.views.delete_scans'),

    url(r'^ajax/location/$', 'inventory.ajax.location_ajax'),

)
