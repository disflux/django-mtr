from django import forms
from django.forms import ModelForm
from parts.models import Part
from reports.models import Report

class NewPartForm(ModelForm):
    class Meta:
        model = Part
        fields = ['part_number', 'description']