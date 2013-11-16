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
    
    def __unicode__(self):
        return "%s: %s pcs" % (self.part, self.inventory_count)
