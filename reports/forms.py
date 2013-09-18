from django import forms
from django.forms import ModelForm
from reports.models import Report, ReportDocument
from parts.models import Part
from vendors.models import Vendor
from django_select2 import *


class PartChoice(AutoModelSelect2Field):
    queryset = Part.objects
    search_fields = ['part_number__istartswith',]
    
class VendorChoice(AutoModelSelect2Field):
    queryset = Vendor.objects
    search_fields = ['name__icontains',]
    
class ReportChoices(AutoModelSelect2MultipleField):
    queryset = Report.objects
    search_fields = ['lot_number__istartswith',]

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['mfg_lot_number', 'vendor_lot_number', 'heat_number',
                  'vendor', 'part_number', 'raw_material', 
                  'origin_po', 'origin_wo', 'linked_reports']
    part_number = PartChoice()
    linked_reports = ReportChoices(required=False)
    vendor = VendorChoice()
    origin_po = forms.CharField(label='Originating PO#', required=False)
    origin_wo = forms.CharField(label='Originating WO#', required=False)
