from django.db import models

from documents.models import Document
from vendors.models import Vendor
from specifications.models import Specification
from parts.models import Part

class Report(models.Model):
    lot_number = models.CharField(max_length=128, null=True, blank=True, editable=False, unique=True)
    mfg_lot_number = models.CharField(max_length=128, null=True, blank=True)
    vendor_lot_number = models.CharField(max_length=128, null=True, blank=True)
    heat_number = models.CharField(max_length=128, null=True, blank=True)
    vendor = models.ForeignKey(Vendor)
    specification = models.ForeignKey(Specification, null=True)
    part_number = models.ForeignKey(Part)
    description = models.TextField()
    origin_po = models.CharField(max_length=32, null=True, blank=True)
    origin_wo = models.CharField(max_length=32, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    documents = models.ManyToManyField(Document,
                                       related_name='attached_documents',
                                       null=True, blank=True)
    linked_reports = models.ManyToManyField('Report',
                                            related_name='report_links',
                                            null=True, blank=True)
    
    def __unicode__(self):
        return self.lot_number

    class Meta:
        unique_together = ('lot_number', 'vendor',)
        
    def save(self, *args, **kwargs):
        import time
        if not self.lot_number:
            self.lot_number = int(time.mktime(time.gmtime()))

        self.mfg_lot_number = self.mfg_lot_number.upper()
        super(Report, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('reports.views.report', [self.lot_number])
    
