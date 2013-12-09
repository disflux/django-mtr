from django.db import models
from parts.models import Part
from django.contrib.auth.models import User

class InventoryLocation(models.Model):
    location_code = models.CharField(max_length=32, unique=True)
    count_complete = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.location_code)
        
    @models.permalink
    def get_absolute_url(self):
        return ('inventory.views.location', [str(self.location_code)])
        
    
class InventoryCount(models.Model):
    part = models.ForeignKey(Part)
    location = models.ForeignKey(InventoryLocation)
    inventory_count = models.IntegerField()
    count_timestamp = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey(User, related_name='count_user')
    audited = models.BooleanField(default=False)
    auditor = models.ForeignKey(User, null=True, related_name='audit_user')
    audit_timestamp = models.DateTimeField(null=True)
    
    class Meta:
        ordering = ['part']
    
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
    
