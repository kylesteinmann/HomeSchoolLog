from django import forms
from .models import Profile, Student

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'first_name', 'last_name', 'state', 'email'

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'first_name', 'last_name', 'state', 'email'

class AddStudentForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'format': '%Y-%m-%d'  # Enforcing YYYY-MM-DD format
        })
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birthdate', 'grade']

class UpdateStudentForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'format': '%Y-%m-%d'  # Enforcing YYYY-MM-DD format
        })
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birthdate', 'grade']