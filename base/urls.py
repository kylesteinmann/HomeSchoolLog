from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView, SignUpView, HomeView
)

app_name = 'base'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]