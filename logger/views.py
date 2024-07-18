from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .forms import LogForm, SubjectForm
from .models import Subject  # Assuming you have a Subject model

class LogsView(LoginRequiredMixin, FormView):
    template_name = 'student_logs.html'
    success_url = reverse_lazy('logger:logs')
    form_class = LogForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'subject_form' not in context:
            context['subject_form'] = SubjectForm()
        if 'log_form' not in context:
            context['log_form'] = LogForm()
        return context

    def post(self, request, *args, **kwargs):
        subject_form = SubjectForm(request.POST)
        log_form = LogForm(request.POST)

        if 'subject_form' in request.POST:
            if subject_form.is_valid():
                # Assuming you have a Subject model
                Subject.objects.create(
                    name=subject_form.cleaned_data['name'],
                    type=subject_form.cleaned_data['type']
                )
                return redirect(self.success_url)
        elif 'log_form' in request.POST:
            if log_form.is_valid():
                log_form.save()  # Save log form data
                return redirect(self.success_url)

        # If the form is invalid, re-render the page with the forms
        return render(request, self.template_name, self.get_context_data())
