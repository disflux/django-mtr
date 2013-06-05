from django import forms
from django.forms import ModelForm
from orders.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'customer_po', 'order_number']
