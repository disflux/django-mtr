from django.contrib import admin
from orders.models import Customer, Order, OrderLineItem

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderLineItem)
