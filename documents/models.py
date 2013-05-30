from django.db import models

class Document(models.Model):
    type = models.ForeignKey('DocumentType')
    file = models.FileField(upload_to='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class DocumentType(models.Model):
    name = models.CharField(max_length=32, null=False)
    description = models.TextField(null=False)

