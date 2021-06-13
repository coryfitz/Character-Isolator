from django import forms

from .models import FilterPreference

class FilterForm(forms.ModelForm):
    class Meta:
        model = FilterPreference
        fields = ['preference']
        labels = {'preference': ''}


