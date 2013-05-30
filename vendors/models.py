from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    country = models.CharField(max_length=32)
