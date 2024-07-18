from . import views
from django.urls import path


app_name = 'logger'

urlpatterns = [
  path('', views.LogsView.as_view(), name='logs'),
]