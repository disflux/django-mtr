from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=50)
    acronym = models.CharField(max_length=10)
    overview = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.acronym)

    
class Specification(models.Model):
    category = models.ForeignKey(Category)
    spec = models.CharField(max_length=25)
    description = models.TextField()
    key_information = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('category', 'spec',)
        ordering = ('spec', )
    
    def __unicode__(self):
        return "%s %s" % (self.category.acronym, self.spec)

    
