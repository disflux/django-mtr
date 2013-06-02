from django.forms import ModelForm
from reports.models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['mfg_lot_number', 'vendor_lot_number', 'heat_number',
                  'vendor', 'specification', 'part_number', 'origin_po',
                  'origin_wo']
