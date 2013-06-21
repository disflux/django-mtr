from django import forms
from django.forms import ModelForm
from orders.models import Order, OrderLineItem

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'customer_po', 'order_number', 'invoice_number',]
        
class NewLineItemForm(ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['line_number', 'report', 'quantity',]
