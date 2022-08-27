from django import forms
from .models import *


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            'name',
            'image',
            'category',
            'service_state',
            'service_city',
            'service_address',
        )


class ContactForm(forms.Form):
    NAME = forms.CharField(required=False,  widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ENTER YOUR NAME',
        'aria-describedby': 'basic-addon2',
    }))
    EMAIL = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ENTER YOUR EMAIL',
        'aria-describedby': 'basic-addon2'
    }))
    MESSAGE = forms.CharField(required=False,  widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'ENTER YOUR MESAGE',
        'aria-describedby': 'basic-addon2',
        'rows': 10,
        'cols': 40,
    }))

class SearchForm(forms.Form):
    service = forms.CharField(required=True)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    use_default_address = forms.BooleanField(required=False)
