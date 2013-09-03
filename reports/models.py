import string, re
import random
from django.contrib.auth.models import User
from django.db import models
from documents.models import Document
from vendors.models import Vendor
from specifications.models import Specification
from parts.models import Part


class Report(models.Model):
    """
    Stores characteristics of a single, self generated lot number.
    """
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
    created_by = models.ForeignKey(User, null=True)
    raw_material = models.BooleanField(default=False, help_text="Check this box if product is raw material")
    documents = models.ManyToManyField(Document,
                                       null=True, blank=True,
                                       through='ReportDocument')
    linked_reports = models.ManyToManyField('Report',
                                            related_name='report_links',
                                            null=True, blank=True)
    
    class Meta:
        ordering = ('lot_number', )
        
    def __unicode__(self):
        return "%s - %s" % (self.lot_number, self.part_number)

    def save(self, *args, **kwargs):
        """
        Sanitizes user inputted data to upper() and assigns a lot number
        """
        self.mfg_lot_number = self.mfg_lot_number.upper()
        self.vendor_lot_number = self.vendor_lot_number.upper()
        self.heat_number = self.heat_number.upper()
        self.origin_po = re.sub(r'([^\s\w]|_)+', ' ', self.origin_po.strip())
        self.origin_po = re.sub(' +', ' ', self.origin_po)
        super(Report, self).save(*args, **kwargs)
        if not self.lot_number:
            self.lot_number = self.id + 10000
            super(Report, self).save(*args, **kwargs)
            
    
    def get_primary_document_url(self):
        """
        Finds the primary document for a report
        """
        docs = ReportDocument.objects.filter(report=self, primary_document=True)
        for doc in docs:
            if doc.primary_document is True:
                return {'uuid': doc.document.uuid, 'url': doc.document.file.url, 'type': doc.internal_cert} 
            
    def get_all_primary_documents(self):
        """
        Finds all primary documents of report and linked reports
        """
        documents = []
        documents.append(self.get_primary_document_url())
        for report in self.linked_reports.all():
            documents.append(report.get_primary_document_url())
        return documents
        
    def po_list(self):
        return self.origin_po.split(' ')    
             
        

    @models.permalink
    def get_absolute_url(self):
        return ('reports.views.report', [self.lot_number])

class ReportDocument(models.Model):
    """
    Stores information about documents attached to a specific report. Related
    to :model:`reports.Report` and :model:`documents.Document`
    
    """
    CERT_TYPES = (
                    ('O', 'Other document'),
                    ('DBA', 'TSA produced DBA'),
                    ('WS', 'TSA produced Weld Stud'),
                )
    report = models.ForeignKey(Report)
    document = models.ForeignKey(Document)
    primary_document = models.BooleanField(default=False)
    attachment_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True)
    internal_cert = models.CharField(max_length=4, choices=CERT_TYPES)
    
    def __unicode__(self):
        return "Report # %s : Document UUID: %s" % (self.report.lot_number, self.document.uuid)

    
