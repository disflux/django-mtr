from django import forms
from parts.models import Part

class ReportForm(forms.Form):
    part = forms.CharField(max_length=48)
    company = forms.CharField(max_length=48)
    desc = forms.CharField(max_length=256, required=False)
    copy_attrs = forms.BooleanField(required=False)
