from django import forms
from django.forms import ModelForm
from parts.models import Part
from vendors.models import Vendor
from django_select2 import *
from inventory.models import InventoryCount
    
class PartChoice(AutoModelSelect2Field):
    queryset = Part.objects
    search_fields = ['part_number__istartswith',]
    
class InventoryForm(ModelForm):
    class Meta:
        model = InventoryCount
        fields = ('part', 'location', 'inventory_count',)
    part = PartChoice()