from django.urls import path
from . import views

app_name = 'api_patients'

urlpatterns = [
    path('', views.patient_list_api, name='patient_list'),
    path('<int:pk>/', views.patient_detail_api, name='patient_detail'),
] 