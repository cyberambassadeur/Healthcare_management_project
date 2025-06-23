from rest_framework import serializers
from .models import (
    MedicalRecord, Consultation, HospitalizationReport,
    ImagingResult, LabResult, Prescription, DiseaseEvolution, Patient
)
from patients.serializers import PatientSerializer # Import PatientSerializer
from users.serializers import CustomUserSerializer # You need to create this in users/serializers.py if it doesn't exist yet!

# --- Nested Serializers for Medical Record Sub-models ---

class ConsultationSerializer(serializers.ModelSerializer):
    doctor = CustomUserSerializer(read_only=True) # Display doctor's details
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['medical_record'] # Set by parent MedicalRecord

class HospitalizationReportSerializer(serializers.ModelSerializer):
    attending_doctor = CustomUserSerializer(read_only=True)
    class Meta:
        model = HospitalizationReport
        fields = '__all__'
        read_only_fields = ['medical_record']

class ImagingResultSerializer(serializers.ModelSerializer):
    radiologist = CustomUserSerializer(read_only=True)
    class Meta:
        model = ImagingResult
        fields = '__all__'
        read_only_fields = ['medical_record']

class LabResultSerializer(serializers.ModelSerializer):
    technician_or_biologist = CustomUserSerializer(read_only=True)
    class Meta:
        model = LabResult
        fields = '__all__'
        read_only_fields = ['medical_record']

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = CustomUserSerializer(read_only=True)
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['medical_record']

class DiseaseEvolutionSerializer(serializers.ModelSerializer):
    doctor = CustomUserSerializer(read_only=True)
    class Meta:
        model = DiseaseEvolution
        fields = '__all__'
        read_only_fields = ['medical_record']

# --- Main MedicalRecord Serializer with Nested Relationships ---

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    recorded_by = CustomUserSerializer(read_only=True) # Display recorded_by user's details

    # Use PrimaryKeyRelatedField for creation/update if you want to select by ID
    # or use WritableNestedSerializer if you want to create/update them inline.
    # For read-only, many=True is important for related sets.
    consultations = ConsultationSerializer(many=True, read_only=True)
    hospitalization_reports = HospitalizationReportSerializer(many=True, read_only=True)
    imaging_results = ImagingResultSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    disease_evolutions = DiseaseEvolutionSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'record_date', 'recorded_by',
            'chief_complaint', 'current_symptoms',
            'consultations', 'hospitalization_reports', 'imaging_results',
            'lab_results', 'prescriptions', 'disease_evolutions'
        ]
        read_only_fields = ['record_date']