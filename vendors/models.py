from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    country = models.CharField(max_length=32)
    created_by = models.ForeignKey(User, null=True)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('vendors.views.vendor', [str(self.id)])
