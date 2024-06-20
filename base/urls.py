from django.contrib import admin
from django.urls import path, include  
from .views import LoginView

app_name = 'base'

urlpatterns = [
  path('login', LoginView.as_view(), name='login')

]