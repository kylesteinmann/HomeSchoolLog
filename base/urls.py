from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    SignUpView, 
    HomeView,
    CreateProfileView,
    ProfileView
)

app_name = 'base'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create_profile/', CreateProfileView.as_view(), name ='create_profile'),
    path('profile/', ProfileView.as_view(), name='profile')
]