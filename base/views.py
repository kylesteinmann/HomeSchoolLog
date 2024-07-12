from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .forms import CreateProfileForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/home.html'
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
    template_name = 'registration/login.html'

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'registration/logged_out.html'

class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('base:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    success_url = reverse_lazy('base:home')  # Redirect to home or any other page after profile creation

    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).exists():
            # Redirect to a different page if the profile already exists
            return redirect('base:home')  # Replace with the appropriate view name or URL
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the profile with the logged-in user
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