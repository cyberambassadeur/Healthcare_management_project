from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalRecordViewSet, ConsultationViewSet, HospitalizationReportViewSet,
    ImagingResultViewSet, LabResultViewSet, PrescriptionViewSet, DiseaseEvolutionViewSet,
    patient_medical_record_list
)

app_name = 'medical_records' # Good practice for namespacing your app's URLs

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'hospitalization-reports', HospitalizationReportViewSet)
router.register(r'imaging-results', ImagingResultViewSet)
router.register(r'lab-results', LabResultViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'disease-evolutions', DiseaseEvolutionViewSet)

urlpatterns = [
    path('my-records/', patient_medical_record_list, name='patient-record-list'),
    path('', include(router.urls)), # All API endpoints for medical_records start here
]