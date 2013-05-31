from django.db import models

from documents.models import Document
from vendors.models import Vendor
from specifications.models import Specification
from parts.models import Part

class Report(models.Model):
    lot_number = models.CharField(max_length=128)
    mfg_lot_number = models.CharField(max_length=128, null=True)
    vendor_lot_number = models.CharField(max_length=128, null=True)
    vendor = models.ForeignKey(Vendor)
    specification = models.ForeignKey(Specification, null=True)
    part_number = models.ForeignKey(Part)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    documents = models.ManyToManyField(Document, related_name='attached_documents')
    
    class Meta:
        unique_together = ('lot_number', 'vendor',)
    
