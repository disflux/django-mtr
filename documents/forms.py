from django.forms import ModelForm
from documents.models import Document

class NewDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['type', 'file']
