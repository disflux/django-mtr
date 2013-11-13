from django.db import models
from parts.models import Part

class InventoryLocation(models.Model):
    location_code = models.CharField(max_length=32)
    
    def __unicode__(self):
        return str(self.location_code)
    
class InventoryCount(models.Model):
    part = models.ForeignKey(Part)
    location = models.ForeignKey(InventoryLocation)
    inventory_count = models.IntegerField()
    
    def __unicode__(self):
        return "%s: %s pcs" % (self.part, self.inventory_count)
