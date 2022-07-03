from django import forms
from .models import *


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            'name',
            'type',
            'price',
            'negotiate',
            'max_negotiation_price',
            'min_negotiation_price',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Enter your service name here',
                    'rows': 10,
                    'cols': 80,
                }
            )

        }


class ContactForm(forms.Form):
    NAME = forms.CharField(required=False)
    EMAIL = forms.CharField(required=False)
    MESSAGE = forms.CharField(required=False)

class SearchForm(forms.Form):
    service = forms.CharField(required=True)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    use_default_address = forms.BooleanField(required=False)
