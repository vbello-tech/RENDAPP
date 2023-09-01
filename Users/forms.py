from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget

class ProfileForm(forms.Form):
        #profile_image = forms.FileField(required=False, widget=forms.FileInput(attrs={
         #   'class': 'form-control',
          #  'placeholder': 'INPUT ADDRESS',
          #  'aria-describedby': 'basic-addon2'
        #}))
        phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget( country_choices=[
                 ("CA", "Canada"),
                 ("NG", "Nigeria"),
                 ('US', 'United States of America')
            ],
            attrs={
                'class': 'form-control',
                'placeholder': 'INPUT PHONE NUMBER',
                'aria-describedby': 'basic-addon2'
            })
        )
        state = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'INPUT YOUR STATE',
            'aria-describedby': 'basic-addon2'
        }))
        city = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'INPUT YOUR CITY',
            'aria-describedby': 'basic-addon2'
        }))

class NewUSerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUSerForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class OnboardForm(forms.ModelForm):
    class Meta:
        model = ServiceOwnerDetails
        fields = "__all__"
