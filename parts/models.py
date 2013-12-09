from django.db import models

from specifications.models import Specification

from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

class Part(models.Model):
    part_number = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    box_quantity = models.IntegerField(null=True, blank=True)
    specification = models.ForeignKey(Specification, null=True)
    product_code = models.CharField(max_length=16, null=True)
    
    class Meta:
        ordering = ('part_number', )
    
    def __unicode__(self):
        return self.part_number

    def save(self, *args, **kwargs):
        self.part_number = self.part_number.upper()
        self.description = self.description.upper()
        super(Part, self).save(*args, **kwargs)
        
    def get_stocking_cost(self):
        from inventory.models import PartValuation
        cost = PartValuation.objects.get(part=self)
        return cost.stocking_cost

    def get_uom(self):
        from inventory.models import PartValuation
        cost = PartValuation.objects.get(part=self)
        return cost.uom        
    @models.permalink
    def get_absolute_url(self):
        return ('parts.views.part', [str(self.part_number)])

        

