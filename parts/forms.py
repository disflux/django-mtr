from django import forms
from django.forms import ModelForm
from parts.models import Part
from vendors.models import Vendor
from django_select2 import *
    
class PartChoice(AutoModelSelect2Field):
    queryset = Part.objects
    search_fields = ['part_number__istartswith',]
    max_results = 10

class NewPartForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewPartForm, self).__init__(*args, **kwargs)
        self.fields['alternate_number'].required = False
            
    class Meta:
        model = Part
        fields = ['part_number', 'alternate_number', 'specification', 'description', 'box_quantity',]
        
class PartLabelForm(forms.Form):
    part_number = PartChoice()
       
