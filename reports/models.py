from django.db import models

from documents.models import Document
from vendors.models import Vendor

class Report(models.Model):
    lot_number = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor)
    specification = models.ForeignKey(Specification, null=True)
    mfg_lot_number = models.CharField(max_length=128, null=True)
    vendor_lot_number = models.CharField(max_length=128, null=True)
    part_number = models.ForeignKey(Part)
    documents = models.ManyToManyField(Document, related_name='attached_documents')
    
    class Meta:
        unique_together = ('lot_number', 'vendor',)
    
