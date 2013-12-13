from django.db import models
from parts.models import Part
from django.db.models import Avg, Sum
from django.contrib.auth.models import User

class InventoryLocation(models.Model):
    location_code = models.CharField(max_length=32, unique=True)
    count_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['location_code']
    
    def __unicode__(self):
        return str(self.location_code)
        
    def check_audits(self):
        no_audit = InventoryCount.objects.filter(location=self, audited=False).count()
        if no_audit > 0:
            return False
        else:
            return True
    
    def scan_count(self):
        return InventoryCount.objects.filter(location=self).count()
        
    def scan_value(self):
        agg = InventoryCount.objects.filter(location=self).aggregate(stocking_value=Sum('stocking_value'), total_parts=Sum('inventory_count'))
        return agg['stocking_value']
        
    @models.permalink
    def get_absolute_url(self):
        return ('inventory.views.location', [str(self.location_code)])
        
    
class InventoryCount(models.Model):
    part = models.ForeignKey(Part)
    location = models.ForeignKey(InventoryLocation)
    inventory_count = models.IntegerField(null=True)
    count_timestamp = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey(User, related_name='count_user', null=True)
    scans = models.IntegerField(null=True)
    audited = models.BooleanField(default=False)
    auditor = models.ForeignKey(User, null=True, related_name='audit_user')
    audit_timestamp = models.DateTimeField(null=True)
    stocking_value = models.DecimalField(null=True, decimal_places=4,
                                         max_digits=12)
    
    class Meta:
        ordering = ['part']

    def save(self, *args, **kwargs):
        self.stocking_value = self.get_scan_value()
        super(InventoryCount, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s: %s pcs" % (self.part, self.inventory_count)

    def get_scan_value(self):
        try:
            cost = PartValuation.objects.get(part=self.part)
            value = self.inventory_count * cost.stocking_cost
        except:
            value = 0
        return value
        
class PartValuation(models.Model):
    part = models.ForeignKey(Part, unique=True)
    uom = models.CharField(max_length=4, null=True)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True)
    stocking_cost = models.DecimalField(decimal_places=4, max_digits=12, null=True)
    ext_value = models.DecimalField(null=True, decimal_places=4, max_digits=12)
    
class InventoryValuation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_parts = models.IntegerField()
    total_valuation = models.DecimalField(decimal_places=4, max_digits=16)
    
