# Create your views here.
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    MedicalRecord, Consultation, HospitalizationReport,
    ImagingResult, LabResult, Prescription, DiseaseEvolution
)
from .serializers import (
    MedicalRecordSerializer, ConsultationSerializer, HospitalizationReportSerializer,
    ImagingResultSerializer, LabResultSerializer, PrescriptionSerializer, DiseaseEvolutionSerializer
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import role_required
from patients.models import Patient

# --- Django REST Framework API ViewSets ---

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def perform_create(self, serializer):
        # Expect patient to be provided in the request data (as patient_id)
        patient_id = self.request.data.get('patient')
        if not patient_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'patient': 'This field is required.'})
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'patient': 'Invalid patient ID.'})
        serializer.save(patient=patient)

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class HospitalizationReportViewSet(viewsets.ModelViewSet):
    queryset = HospitalizationReport.objects.all()
    serializer_class = HospitalizationReportSerializer

class ImagingResultViewSet(viewsets.ModelViewSet):
    queryset = ImagingResult.objects.all()
    serializer_class = ImagingResultSerializer

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class DiseaseEvolutionViewSet(viewsets.ModelViewSet):
    queryset = DiseaseEvolution.objects.all()
    serializer_class = DiseaseEvolutionSerializer

@login_required
@role_required(['patient'])
def patient_medical_record_list(request):
    """
    Display a list of all medical records for the currently logged-in patient.
    """
    try:
        patient_profile = request.user.patient_profile
        records = MedicalRecord.objects.filter(patient=patient_profile)
    except AttributeError:
        messages.error(request, "Your user profile is not linked to a patient profile.")
        records = MedicalRecord.objects.none()

    context = {
        'medical_records': records,
        'title': 'My Medical Records'
    }
    return render(request, 'medical_records/record_list.html', context)

@login_required
def patient_record_list(request):
    patient = get_object_or_404(Patient, user=request.user)
    record_type = request.GET.get('type')
    if record_type == 'lab':
        records = LabResult.objects.filter(medical_record__patient=patient)
        template = 'medical_records/lab_results_list.html'
    elif record_type == 'prescription':
        records = Prescription.objects.filter(medical_record__patient=patient)
        template = 'medical_records/prescriptions_list.html'
    else:
        records = MedicalRecord.objects.filter(patient=patient)
        template = 'medical_records/record_list.html'
    return render(request, template, {'records': records})

# API views for REST endpoints
@api_view(['GET'])
def medical_record_list_api(request):
    records = MedicalRecord.objects.all()
    serializer = MedicalRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def medical_record_detail_api(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    serializer = MedicalRecordSerializer(record)
    return Response(serializer.data)