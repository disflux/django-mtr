from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'orders.views.orders_index'),
    
    url(r'^new_order/$', 'orders.views.new_order'),

    url(r'^(?P<order_number>\w+)$', 'orders.views.order'),
)
