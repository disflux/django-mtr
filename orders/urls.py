from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'orders.views.orders_index'),
    
    url(r'^new_order/$', 'orders.views.new_order'),
    
    url(r'^certs/(?P<order_number>\d+)$', 'pdfgen.cert_packet.generate_cert_packet'),
    

    url(r'^(?P<order_number>\w+)$', 'orders.views.order'),
)
