from django.db import models

class Part(models.Model):
    part_number = models.CharField(max_length=128, null=True)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('part_number', )
    
    def __unicode__(self):
        return self.part_number

    def save(self, *args, **kwargs):
        self.part_number = self.part_number.upper()
        super(Part, self).save(*args, **kwargs)

        

