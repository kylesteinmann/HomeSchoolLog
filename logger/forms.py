from .models import Log, Subject, RequiredSubjects
from base.models import Profile, Student
from django import forms
from django.db.models import Q

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'type']


class LogForm(forms.Form):
    subject = forms.ChoiceField(choices=[])
    time_spent = forms.DecimalField(decimal_places=1, max_digits=10)
    location = forms.CharField(max_length=100, widget=forms.Select(choices=[('Home', 'Home'), ('Away', 'Away')]))
    description = forms.CharField(max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    student = forms.ModelChoiceField(queryset=Student.objects.none())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LogForm, self).__init__(*args, **kwargs)

        if self.request:
            user_subjects = Subject.objects.filter(user=self.request.user).values_list('name', flat=True)
            required_subjects = RequiredSubjects.objects.all().values_list('name', flat=True)
            
            combined_subjects = set(user_subjects).union(set(required_subjects))
            queryset = [(subject, subject) for subject in combined_subjects]
            
            self.fields['subject'].choices = queryset
            self.fields['student'].queryset = Student.objects.filter(user=self.request.user)
