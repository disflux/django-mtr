from django.db import models
from uuidfield import UUIDField
from sorl.thumbnail import ImageField

def document_file_name(instance, filename):
    import os
    name, ext = os.path.splitext(filename)
    path = 'documents/%s%s' % (str(instance.uuid), ext)
    return path

class Document(models.Model):
    uuid = UUIDField(auto=True)
    type = models.ForeignKey('DocumentType')
    file = models.FileField(upload_to=document_file_name, null=True)
    document_hash = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.uuid)
        
    @models.permalink
    def get_absolute_url(self):
        return ('documents.views.document', [str(self.uuid)])

class DocumentType(models.Model):
    name = models.CharField(max_length=32, null=False)
    description = models.TextField(null=False)

    def __unicode__(self):
        return self.name

