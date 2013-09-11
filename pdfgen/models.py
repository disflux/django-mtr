from django.db import models


class TemplateField(models.Model):
    FIELD_CHOICES = (
                        ('LINE', 'LINE'),
                        ('TEXT', 'TEXT'),
                        ('BARCODE', 'BARCODE'),
                    )
    type = models.CharField(max_length=10, choices=FIELD_CHOICES)
    start_x = models.FloatField(null=True, blank=True)
    start_y = models.FloatField(null=True, blank=True)
    end_x = models.FloatField(null=True, blank=True)
    end_y = models.FloatField(null=True, blank=True)
    fill_color = models.CharField(max_length=16, null=True, default='black')
    text_size = models.IntegerField(null=True, default=12)
    text_centered = models.BooleanField(default=True)
    text = models.CharField(max_length=128, null=True, blank=True)
    
    def __unicode__(self):
        return self.type
     
class PDFTemplate(models.Model):
    name = models.CharField(max_length=64)
    fields = models.ManyToManyField(TemplateField, related_name='template_field')
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    file = models.FileField(upload_to='pdf_templates', null=True, blank=True)
    
    def __unicode__(self):
        return self.name
