from django.shortcuts import render
from django.views.generic import FormView


class LoginView(FormView):
  template_name = 'base/login.html'