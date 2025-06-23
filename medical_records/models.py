# medical_records/models.py
# Create your models here.
from django.db import models
from patients.models import Patient
from users.models import CustomUser # Ensure this is your custom user model
from django.utils.translation import gettext_lazy as _
import uuid # For unique IDs for records

class MedicalRecord(models.Model):
    """
    Central model for a patient's medical dossier.
    This acts as a container for all related medical information.
    """
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name=_("Patient")
    )
    # This field could be an overview or initial assessment
    record_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Record Date"))
    recorded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role__in' to 'user_type__in'
        limit_choices_to={'user_type__in': ['doctor', 'admin', 'staff', 'pharmacist']}, # Only medical professionals based on CustomUser roles
        verbose_name=_("Recorded By")
    )
    chief_complaint = models.TextField(blank=True, null=True, verbose_name=_("Chief Complaint"))
    current_symptoms = models.TextField(blank=True, null=True, verbose_name=_("Current Symptoms"))
    # Add other general medical record fields as needed
    allergies = models.TextField(blank=True, null=True, verbose_name=_("Allergies"))

    def __str__(self):
        return f"Medical Record for {self.patient.first_name} {self.patient.last_name} ({self.record_date.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = _("Medical Record")
        verbose_name_plural = _("Medical Records")
        ordering = ['-record_date'] # Order by most recent

class Consultation(models.Model):
    """
    Details of a specific consultation.
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='consultations',
        verbose_name=_("Medical Record")
    )
    consultation_date = models.DateTimeField(verbose_name=_("Consultation Date"))
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role' to 'user_type'
        limit_choices_to={'user_type': 'doctor'},
        related_name='consultations',
        verbose_name=_("Consulting Doctor")
    )
    diagnosis = models.TextField(verbose_name=_("Diagnosis"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    follow_up_date = models.DateField(blank=True, null=True, verbose_name=_("Follow-up Date"))

    def __str__(self):
        return f"Consultation on {self.consultation_date.strftime('%Y-%m-%d')} for {self.medical_record.patient.last_name}"

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")
        ordering = ['-consultation_date']

class HospitalizationReport(models.Model):
    """
    Reports for hospitalizations or surgeries.
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='hospitalization_reports',
        verbose_name=_("Medical Record")
    )
    admission_date = models.DateField(verbose_name=_("Admission Date"))
    discharge_date = models.DateField(blank=True, null=True, verbose_name=_("Discharge Date"))
    reason_for_admission = models.TextField(verbose_name=_("Reason for Admission"))
    procedure_performed = models.TextField(blank=True, null=True, verbose_name=_("Procedure Performed"))
    report_details = models.TextField(verbose_name=_("Report Details"))
    attending_doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role' to 'user_type'
        limit_choices_to={'user_type': 'doctor'},
        related_name='hospitalization_reports',
        verbose_name=_("Attending Doctor")
    )

    def __str__(self):
        return f"Hospitalization for {self.medical_record.patient.last_name} from {self.admission_date}"

    class Meta:
        verbose_name = _("Hospitalization Report")
        verbose_name_plural = _("Hospitalization Reports")
        ordering = ['-admission_date']

class ImagingResult(models.Model):
    """
    Stores imaging results (radios, ultrasounds, etc.).
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='imaging_results',
        verbose_name=_("Medical Record")
    )
    imaging_type = models.CharField(
        max_length=50,
        choices=[('xray', 'X-Ray'), ('ultrasound', 'Ultrasound'), ('mri', 'MRI'), ('ct_scan', 'CT Scan'), ('other', 'Other')],
        verbose_name=_("Imaging Type")
    )
    scan_date = models.DateField(verbose_name=_("Scan Date"))
    # Using ImageField requires `Pillow` library: `pip install Pillow`
    image_file = models.ImageField(upload_to='imaging_results/', blank=True, null=True, verbose_name=_("Image File"))
    report = models.FileField(upload_to='imaging_reports/', blank=True, null=True, verbose_name=_("Report File (PDF)"))
    conclusion = models.TextField(verbose_name=_("Conclusion"))
    radiologist = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role' to 'user_type'
        limit_choices_to={'user_type': 'doctor'}, # Or a specific radiologist role if you define one
        related_name='imaging_readings',
        verbose_name=_("Radiologist")
    )

    def __str__(self):
        return f"{self.imaging_type} for {self.medical_record.patient.last_name} on {self.scan_date}"

    class Meta:
        verbose_name = _("Imaging Result")
        verbose_name_plural = _("Imaging Results")
        ordering = ['-scan_date']

class LabResult(models.Model):
    """
    Stores laboratory test results.
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='lab_results',
        verbose_name=_("Medical Record")
    )
    analysis_type = models.CharField(max_length=100, verbose_name=_("Type of Analysis"))
    measured_value = models.CharField(max_length=255, verbose_name=_("Measured Value")) # Store as string for flexibility (e.g., "1.2 mmol/L", "Positive")
    reference_value = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Reference Value"))
    conclusion = models.TextField(blank=True, null=True, verbose_name=_("Biologist's Conclusion"))
    sample_collection_date = models.DateTimeField(verbose_name=_("Sample Collection Date"))
    result_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Result Date"))
    laboratory_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Laboratory Name"))
    technician_or_biologist = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role__in' to 'user_type__in'
        limit_choices_to={'user_type__in': ['staff', 'doctor']}, # Assuming 'staff' can be lab_tech
        related_name='lab_test_entries',
        verbose_name=_("Technician/Biologist")
    )
    result_file = models.FileField(upload_to='lab_results/', blank=True, null=True, verbose_name=_("Result File (e.g., PDF)"))

    def __str__(self):
        return f"Lab Result ({self.analysis_type}) for {self.medical_record.patient.last_name} on {self.result_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = _("Laboratory Result")
        verbose_name_plural = _("Laboratory Results")
        ordering = ['-result_date']

class Prescription(models.Model):
    """
    Details of a medical prescription.
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_("Medical Record")
    )
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role' to 'user_type'
        limit_choices_to={'user_type': 'doctor'},
        related_name='prescriptions_made',
        verbose_name=_("Prescribing Doctor")
    )
    prescription_date = models.DateField(auto_now_add=True, verbose_name=_("Prescription Date"))
    medications = models.TextField(
        help_text=_("List medications with name, dosage, duration (e.g., 'Paracetamol 500mg, 1 tablet 3x/day for 5 days')"),
        verbose_name=_("Medications")
    )
    complementary_exams = models.TextField(
        blank=True, null=True,
        help_text=_("E.g., 'Blood work (CBC, Glucose)', 'Chest X-Ray'"),
        verbose_name=_("Complementary Exams")
    )
    medical_advice = models.TextField(
        blank=True, null=True,
        help_text=_("E.g., 'Rest for 3 days', 'Low-sodium diet', 'Avoid strenuous activity'"),
        verbose_name=_("Medical Advice/Instructions")
    )
    is_signed = models.BooleanField(default=True, verbose_name=_("Is Signed"))

    def __str__(self):
        return f"Prescription by Dr. {self.doctor.last_name} for {self.medical_record.patient.last_name} on {self.prescription_date}"

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")
        ordering = ['-prescription_date']

class DiseaseEvolution(models.Model):
    """
    Tracks the evolution of a patient's disease.
    """
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='disease_evolutions',
        verbose_name=_("Medical Record")
    )
    evolution_date = models.DateField(auto_now_add=True, verbose_name=_("Evolution Date"))
    observations = models.TextField(verbose_name=_("Observations"))
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        # Changed 'role' to 'user_type'
        limit_choices_to={'user_type': 'doctor'},
        related_name='disease_evolution_entries',
        verbose_name=_("Observed By Doctor")
    )

    def __str__(self):
        return f"Disease Evolution for {self.medical_record.patient.last_name} on {self.evolution_date}"

    class Meta:
        verbose_name = _("Disease Evolution")
        verbose_name_plural = _("Disease Evolutions")
        ordering = ['-evolution_date']