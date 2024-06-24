from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/home.html'
    login_url = '/login'

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
