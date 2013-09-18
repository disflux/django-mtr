from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from uuidfield import UUIDField
from sorl.thumbnail import ImageField

def document_file_name(instance, filename):
    import os
    name, ext = os.path.splitext(filename)
    path = 'documents/%s%s' % (str(instance.uuid), ext)
    return path

def count_pages(sender, instance, created, **kwargs):
    if created:
        import re
        import urllib2
        rxcountpages = re.compile(r"$\s*/Type\s*/Page[/\s]", re.MULTILINE|re.DOTALL)
        data = urllib2.urlopen(instance.file.url,"rb").read()
        return ln(rxcountpages.findall(data))

class Document(models.Model):
    uuid = UUIDField(auto=True)
    type = models.ForeignKey('DocumentType')
    file = models.FileField(upload_to=document_file_name, null=True)
    document_hash = models.CharField(max_length=1000, null=True)
    pages = models.IntegerField(max_length=3, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        if not self.pages:
            from pyPdf import PdfFileReader, PdfFileWriter
            from StringIO import StringIO
            from urllib2 import Request, urlopen
            f = urlopen(Request(self.file.url)).read()
            mem = StringIO(f)
            pdf = PdfFileReader(mem)
            self.pages = pdf.getNumPages()
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('documents.views.document', [str(self.uuid)])

class DocumentType(models.Model):
    name = models.CharField(max_length=32, null=False)
    description = models.TextField(null=False)
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return str(self.name)


