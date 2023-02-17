from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'profile_pic',
            'phone_number',
            'state',
            'city',
            'address',
            'is_a_provider',
        )

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
