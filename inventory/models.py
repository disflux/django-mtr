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
        
    def get_combined_part_count(self):
        parts = InventoryCount.objects.filter(part=self.part).aggregate(total_count=Sum('inventory_count'))
        return parts['total_count']
        
    def get_combined_inventory_value(self):
        parts = InventoryCount.objects.filter(part=self.part).aggregate(value=Sum('stocking_value'))
        return parts['value']
        
    def get_pre_inventory_count(self):
        part = PartValuation.objects.get(part=self.part)
        return part.quantity
        
    def get_pre_inventory_value(self):
        part = PartValuation.objects.get(part=self.part)
        return part.ext_value
    
    def get_applied_quantity(self):
        part = PartValuation.objects.get(part=self.part)
        return part.applied_quantity
        
    def get_difference(self):
        post = self.get_combined_part_count()
        pre = self.get_pre_inventory_count()
        return post - pre
        
    def get_dollar_difference(self):
        post = self.get_combined_inventory_value()
        pre = self.get_pre_inventory_value()
        
        return post - pre
        
    def get_on_reserve(self):
        pv = PartValuation.objects.get(part=self.part)
        return pv.applied_quantity
    
    def get_less_reserve(self):
        return self.inventory_count - self.get_on_reserve()
        
        
        
        
class PartValuation(models.Model):
    part = models.ForeignKey(Part, unique=True)
    uom = models.CharField(max_length=4, null=True)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True)
    applied_quantity = models.IntegerField(null=True, default=0)
    stocking_cost = models.DecimalField(decimal_places=4, max_digits=12, null=True)
    ext_value = models.DecimalField(null=True, decimal_places=4, max_digits=12)
    
    class Meta:
        ordering = ['part']
    
    def __unicode__(self):
        return "%s (pcs: %s)" % (self.part.part_number, self.quantity)
    
class InventoryValuation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_parts = models.IntegerField()
    total_valuation = models.DecimalField(decimal_places=4, max_digits=16)
    
