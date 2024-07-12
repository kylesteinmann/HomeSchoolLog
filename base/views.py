from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, FormView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Student
from .forms import CreateProfileForm, UpdateProfileForm, AddStudentForm



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login'  # You can use `login_url = reverse_lazy('login')` if you prefer

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Redirect to a different page if the profile does not exist
            return redirect('base:create_profile')  # Replace with your profile creation view name
        return super(HomeView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs, ):
        context = super().get_context_data(**kwargs)
        # Add custom context variables here
        context['profile_info'] = Profile.objects.get(user=self.request.user)
        
        return context
    
class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'logged_out.html'

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('base:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    success_url = reverse_lazy('base:home')  

    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).exists():
            return redirect('base:home')  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = request.user
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Student
from .forms import UpdateProfileForm, AddStudentForm

class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('base:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_info'] = get_object_or_404(Profile, user=self.request.user)
        context['student_info'] = Student.objects.filter(user=self.request.user)
        context['add_student_form'] = AddStudentForm()
        context['edit_student_form'] = AddStudentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'edit_profile' in request.POST:
            if form.is_valid():
                instance = Profile.objects.get(user=self.request.user)
                instance.first_name = form.cleaned_data['first_name']
                instance.last_name = form.cleaned_data['last_name']
                instance.state = form.cleaned_data['state']
                instance.email = form.cleaned_data['email']
                instance.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        if 'add_student' in request.POST:
            add_student_form = AddStudentForm(request.POST)
            if add_student_form.is_valid():
                student = Student(
                    first_name=add_student_form.cleaned_data['first_name'],
                    last_name=add_student_form.cleaned_data['last_name'],
                    birthdate=add_student_form.cleaned_data['birthdate'],
                    grade=add_student_form.cleaned_data['grade'],
                    user=self.request.user
                )
                student.save()
                return self.form_valid(add_student_form)
            else:
                return self.form_invalid(add_student_form)
        
        if 'update_student' in request.POST:
            student_id = request.POST.get('student_id')
            student_instance = Student.objects.get(id=student_id)
            edit_student_form = AddStudentForm(request.POST, instance=student_instance)
            if edit_student_form.is_valid():
                edit_student_form.save()
                return self.form_valid(edit_student_form)
            else:
                return self.form_invalid(edit_student_form)

        return super().post(request, *args, **kwargs)

