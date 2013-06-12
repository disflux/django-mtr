from django.contrib.auth.models import User
from django.db import models

from reports.models import Report
from documents.models import Document


class Customer(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer)
    customer_po = models.CharField(max_length=32)
    order_number = models.CharField(max_length=16)
    line_items = models.ManyToManyField('OrderLineItem', related_name='order_line_items', null=True, blank=True)
    documents = models.ManyToManyField(Document, related_name='order_documents', null=True, blank=True)
    created_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.order_number
        
    @models.permalink
    def get_absolute_url(self):
        return ('orders.views.order', [self.order_number])

    def save(self, *args, **kwargs):
        self.customer_po = self.customer_po.upper()
        super(Order, self).save(*args, **kwargs)
    
    
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order)
    line_number = models.IntegerField(max_length=4, help_text="Line number on the work order")
    report = models.ForeignKey(Report, blank=True, null=True, help_text="Report Lot #")
    
    class Meta:
        ordering = ('line_number',)
