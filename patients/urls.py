from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, patient_list, edit_patient_profile # Import the new view

app_name = 'patients' # Good practice for namespacing your app's URLs

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/patients', PatientViewSet, basename='patient-api') # This creates /api/patients/ and /api/patients/{id}/ endpoints

urlpatterns = [
    # You can add a regular home view here if needed, e.g., path('', views.home, name='home'),
    path('list/', patient_list, name='patient-list-html'), # URL for the HTML patient list
    path('profile/edit/', edit_patient_profile, name='edit-profile'), # URL for editing patient profile
    path('', include(router.urls)), # DRF API endpoints
]