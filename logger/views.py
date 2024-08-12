from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from collections import defaultdict


from datetime import timedelta
from django.utils import timezone

from base.models import Profile, Student
from .forms import LogForm, SubjectForm
from .models import RequiredSubjects, Subject, Log

class LogsView(LoginRequiredMixin, FormView):
    template_name = 'student_logs.html'
    success_url = reverse_lazy('logger:logs')
    form_class = LogForm
    profile_model = Profile
    subject_model = Subject
    required_subjects_model = RequiredSubjects
    student_model = Student
    log_model = Log

    def get_form_kwargs(self):
        kwargs = super(LogsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        today = timezone.now().date()
        days_since_sunday = today.weekday() + 1 
        most_recent_sunday = today - timedelta(days=days_since_sunday) 

        weekly_logs = self.log_model.objects.filter(
            user=self.request.user,
            date__gte=most_recent_sunday,
            date__lte=most_recent_sunday + timedelta(days=6)
        ).order_by('date')

        daily_log_info = self.log_model.objects.filter( user=self.request.user,
            date = today)

        grouped_weekly_logs = defaultdict(list)
        for log in weekly_logs:
            grouped_weekly_logs[log.date].append(log)

        if 'subject_form' not in context:
            context['subject_form'] = SubjectForm()

        if 'log_form' not in context:
            context['log_form'] = self.get_form()
        
        context['daily_log_info'] = daily_log_info
        context['grouped_weekly_logs'] = dict(grouped_weekly_logs)
        context['most_recent_sunday'] = most_recent_sunday
        context['student_info'] = Student.objects.filter(user=self.request.user)
        
        return context

    def post(self, request, *args, **kwargs):
        subject_form = SubjectForm(request.POST)
        log_form = self.get_form()

        if 'subject_form' in request.POST:
            if subject_form.is_valid():
                Subject.objects.create(
                    name=subject_form.cleaned_data['name'],
                    type=subject_form.cleaned_data['type'],
                    user=self.request.user
                )
                return redirect(self.success_url)
        elif 'log_form' in request.POST:
            if log_form.is_valid():
                subject_name = log_form.cleaned_data['subject']
                
                try:
                    if subject_name in self.subject_model.objects.filter(user=self.request.user).values_list('name', flat=True):
                        subject = self.subject_model.objects.get(user=self.request.user, name=subject_name)
                        required_subject = None
                    else:
                        required_subject = self.required_subjects_model.objects.get(name=subject_name)
                        subject = None

                    hour_type = 'Core' if required_subject else 'Elective'
                    
                    log = self.log_model.objects.create(
                        student=log_form.cleaned_data['student'],
                        user=self.request.user,
                        subject=subject,
                        required_subject=required_subject,
                        time_spent=log_form.cleaned_data['time_spent'],
                        hour_type=hour_type,
                        location=log_form.cleaned_data['location'],
                        date=log_form.cleaned_data['date'],
                        description=log_form.cleaned_data['description']
                    )
                    log.save()

                    for log in self.log_model.objects.all():
                        print(log.__dict__)

                    return redirect(self.success_url)

                except self.required_subjects_model.DoesNotExist:
                    return self.form_invalid(log_form, error_message="The subject does not exist.")
        
        return render(request, self.template_name, self.get_context_data())

