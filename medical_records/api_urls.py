from django.urls import path
from . import views

app_name = 'api_medical_records'

urlpatterns = [
    path('', views.medical_record_list_api, name='medical_record_list'),
    path('<int:pk>/', views.medical_record_detail_api, name='medical_record_detail'),
] 