# Register your models here.
from django.contrib import admin
from .models import (
    MedicalRecord, Consultation, HospitalizationReport,
    ImagingResult, LabResult, Prescription, DiseaseEvolution
)
from django.utils.translation import gettext_lazy as _

# Inline classes for related models to be displayed within MedicalRecord admin
class ConsultationInline(admin.TabularInline):
    model = Consultation
    extra = 1 # Number of empty forms to display

class HospitalizationReportInline(admin.TabularInline):
    model = HospitalizationReport
    extra = 0 # Don't show empty forms by default
    show_change_link = True # Allow editing existing inline objects

class ImagingResultInline(admin.TabularInline):
    model = ImagingResult
    extra = 0
    show_change_link = True

class LabResultInline(admin.TabularInline):
    model = LabResult
    extra = 0
    show_change_link = True

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1
    show_change_link = True

class DiseaseEvolutionInline(admin.TabularInline):
    model = DiseaseEvolution
    extra = 1
    show_change_link = True

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_date', 'recorded_by', 'chief_complaint')
    search_fields = ('patient__first_name', 'patient__last_name', 'chief_complaint')
    list_filter = ('record_date', 'recorded_by__user_type')
    raw_id_fields = ('patient', 'recorded_by') # Use raw_id_fields for FKs to show ID input, better for large datasets
    inlines = [
        ConsultationInline,
        HospitalizationReportInline,
        ImagingResultInline,
        LabResultInline,
        PrescriptionInline,
        DiseaseEvolutionInline,
    ]
    fieldsets = (
        (None, {'fields': ('patient', 'recorded_by', 'record_date')}),
        (_("Medical Details"), {'fields': ('chief_complaint', 'current_symptoms')}),
    )
    readonly_fields = ('record_date',)

# Register other models separately for individual management if needed
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'consultation_date', 'doctor', 'diagnosis')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'diagnosis')
    list_filter = ('consultation_date', 'doctor')
    raw_id_fields = ('medical_record', 'doctor')

@admin.register(HospitalizationReport)
class HospitalizationReportAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'admission_date', 'discharge_date', 'attending_doctor')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'reason_for_admission')
    list_filter = ('admission_date', 'attending_doctor')
    raw_id_fields = ('medical_record', 'attending_doctor')


@admin.register(ImagingResult)
class ImagingResultAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'imaging_type', 'scan_date', 'radiologist')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'imaging_type')
    list_filter = ('imaging_type', 'scan_date', 'radiologist')
    raw_id_fields = ('medical_record', 'radiologist')


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'analysis_type', 'measured_value', 'result_date', 'laboratory_name', 'technician_or_biologist')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'analysis_type', 'laboratory_name')
    list_filter = ('analysis_type', 'result_date', 'laboratory_name')
    raw_id_fields = ('medical_record', 'technician_or_biologist')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'doctor', 'prescription_date', 'is_signed')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'medications')
    list_filter = ('prescription_date', 'doctor', 'is_signed')
    raw_id_fields = ('medical_record', 'doctor')


@admin.register(DiseaseEvolution)
class DiseaseEvolutionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'evolution_date', 'doctor')
    search_fields = ('medical_record__patient__first_name', 'medical_record__patient__last_name', 'observations')
    list_filter = ('evolution_date', 'doctor')
    raw_id_fields = ('medical_record', 'doctor')
