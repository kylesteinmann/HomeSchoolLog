from collections import defaultdict
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import  Subject, RequiredSubjects,  Log
from base.models import Profile, Student
from .forms import LogForm, SubjectForm
from django.contrib.auth.mixins import LoginRequiredMixin

class LogsView(LoginRequiredMixin, FormView):
    template_name = 'student_logs.html'
    success_url = reverse_lazy('logger:logs')
    form_class = LogForm

    def get_form_kwargs(self):
        kwargs = super(LogsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Initialize models only once
        self.profile_model = Profile.objects.filter(user=self.request.user)
        self.subject_model = Subject.objects.filter(user=self.request.user)
        self.required_subjects_model = RequiredSubjects.objects.all()
        self.student_model = Student.objects.filter(user=self.request.user)
        self.log_model = Log.objects.filter(user=self.request.user)

        today = timezone.now().date()

        selected_day_str = self.request.GET.get('date', today.isoformat())
        selected_tab = self.request.GET.get('tab', 'daily-log')

        try:
            selected_day = datetime.strptime(selected_day_str, '%Y-%m-%d').date()
        except ValueError:
            selected_day = today

        selected_week = selected_day - timedelta(days=selected_day.weekday() + 1)
        previous_week = selected_week - timedelta(days=7)
        next_week = selected_week + timedelta(days=7)

        weekly_logs = self.log_model.filter(
            date__gte=selected_week,
            date__lte=selected_week + timedelta(days=6)
        ).order_by('date')

        daily_log_info = self.log_model.filter(date=selected_day)
        grouped_weekly_logs = defaultdict(list)

        for log in weekly_logs:
            grouped_weekly_logs[log.date].append(log)

        if 'subject_form' not in context:
            context['subject_form'] = SubjectForm()

        if 'log_form' not in context:
            context['log_form'] = self.get_form()
        
        context.update({
            'daily_log_info': daily_log_info,
            'grouped_weekly_logs': dict(grouped_weekly_logs),
            'most_recent_sunday': selected_week,
            'previous_day': selected_day - timedelta(days=1),
            'next_day': selected_day + timedelta(days=1),
            'previous_week': previous_week,
            'next_week': next_week,
            'student_info': self.student_model,
            'selected_tab': selected_tab,
        })

        return context

    def post(self, request, *args, **kwargs):
        subject_form = SubjectForm(request.POST)
        log_form = self.get_form()

        if 'subject_form' in request.POST:
            if subject_form.is_valid():
                subject = Subject(
                    name=subject_form.cleaned_data['name'],
                    type=subject_form.cleaned_data['type'],
                    user=self.request.user
                )
                subject.save()
                return redirect(self.success_url)
            else:
                return self.form_invalid(subject_form)
        
        elif 'log_form' in request.POST:
            if log_form.is_valid():
                subject_name = log_form.cleaned_data['subject']
                
                try:
                    subject = self.subject_model.filter(name=subject_name).first()
                    required_subject = self.required_subjects_model.filter(name=subject_name).first()

                    if not subject and not required_subject:
                        return self.form_invalid(log_form, error_message="The subject does not exist.")

                    hour_type = 'Core' if required_subject else 'Elective'

                    log = Log(
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
                    return redirect(self.success_url)

                except Exception as e:
                    return self.form_invalid(log_form, error_message=str(e))

        return render(request, self.template_name, self.get_context_data())

