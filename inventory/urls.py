from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'inventory.views.inventory_index'),
    url(r'^new_count/$', 'inventory.views.new_count'),

)