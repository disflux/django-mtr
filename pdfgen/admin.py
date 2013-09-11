from django.contrib import admin
from pdfgen.models import PDFTemplate, TemplateField

admin.site.register(PDFTemplate)
admin.site.register(TemplateField)
