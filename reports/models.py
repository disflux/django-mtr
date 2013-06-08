import string
import random

from django.db import models
from documents.models import Document
from vendors.models import Vendor
from specifications.models import Specification
from parts.models import Part


class Report(models.Model):
    lot_number = models.CharField(max_length=128, null=True, blank=True, editable=False, unique=True)
    mfg_lot_number = models.CharField(max_length=128, null=True, blank=True, help_text="The manufacturer's lot number (if available)")
    vendor_lot_number = models.CharField(max_length=128, null=True, blank=True, help_text="The vendor's lot number (if available)")
    heat_number = models.CharField(max_length=128, null=True, blank=True, help_text="The heat number (if available)")
    vendor = models.ForeignKey(Vendor, help_text="Vendor or Manufacturer who supplied the material")
    specification = models.ForeignKey(Specification, null=True)
    part_number = models.ForeignKey(Part, help_text="The TSA part number")
    description = models.TextField()
    origin_po = models.CharField(max_length=32, null=True, blank=True, help_text="The purchase order # material was purchased on")
    origin_wo = models.CharField(max_length=32, null=True, blank=True, help_text="The work order # material was produced from")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    documents = models.ManyToManyField(Document,
                                       null=True, blank=True,
                                       through='ReportDocument')
    linked_reports = models.ManyToManyField('Report',
                                            related_name='report_links',
                                            null=True, blank=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.lot_number, self.part_number)

    def save(self, *args, **kwargs):
        self.mfg_lot_number = self.mfg_lot_number.upper()
        self.vendor_lot_number = self.vendor_lot_number.upper()
        self.heat_number = self.heat_number.upper()
        super(Report, self).save(*args, **kwargs)
        if not self.lot_number:
            self.lot_number = self.id + 10000
            super(Report, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('reports.views.report', [self.lot_number])

class ReportDocument(models.Model):
    report = models.ForeignKey(Report)
    document = models.ForeignKey(Document)
    primary_document = models.BooleanField(default=False)
    attachment_date = models.DateTimeField(auto_now_add=True)

    
