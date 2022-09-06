from django import forms
from .models import *


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