from django import forms
from django.forms import ModelForm
from parts.models import Part
from vendors.models import Vendor
from django_select2 import *
from inventory.models import InventoryCount, InventoryLocation
    
class PartChoice(AutoModelSelect2Field):
    queryset = Part.objects
    search_fields = ['part_number__istartswith',]
    
class LocationChoice(AutoModelSelect2Field):
    queryset = InventoryLocation.objects
    search_fields = ['location_code__istartswith',]
    
class InventoryForm(forms.Form):
    part = forms.CharField()
    location = forms.CharField()
    inventory_count = forms.IntegerField()
    
class DirectToLocationForm(forms.Form):
    location = LocationChoice()
    
class DirectToPartForm(forms.Form):
    part = PartChoice()
