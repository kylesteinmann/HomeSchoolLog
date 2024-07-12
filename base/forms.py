from django import forms
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'first_name', 'last_name', 'state', 'email'