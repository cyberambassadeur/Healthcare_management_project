# core/urls.py

from django.urls import path
from . import views

app_name = 'core' # Good practice for namespacing your app's URLs

urlpatterns = [
    # Define your core/dashboard URLs here later, e.g.:
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]