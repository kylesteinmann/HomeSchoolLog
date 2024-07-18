from .models import Log, Subject
from django import forms

class SubjectForm(forms.ModelForm):
  class Meta:
    model = Subject
    fields = ['name', 'type']

class LogForm(forms.ModelForm):
  subject = forms.ModelChoiceField(queryset=Subject.objects.all())

  class Meta:
    model = Log
    fields = ['subject','time_spent', 'hour_type', 'discription', 'date']

  


