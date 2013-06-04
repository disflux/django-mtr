from django.db import models

from reports.models import Report


class Customer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer)
    customer_po = models.CharField(max_length=32)
    order_number = models.CharField(max_length=16)
    line_items = models.ManyToManyField('OrderLineItem', related_name='order_line_items')
    
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order)
    line_number = models.IntegerField(max_length=4)
    report = models.ForeignKey(Report)
