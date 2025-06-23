# Create your models here.
from django.db import models
from users.models import CustomUser
import uuid # For unique patient ID
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):
    """
    Represents a patient's profile.
    """
    # Link to the CustomUser model if the patient has an account
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL, # If user is deleted, patient profile remains, but link is removed
        null=True, blank=True,
        related_name='patient_profile',
        verbose_name=_("Associated User Account")
    )

    # Basic Patient Profile (Profil de patient)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        verbose_name=_("Gender")
    )
    address = models.TextField(verbose_name=_("Address"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))

    blood_group = models.CharField(
        max_length=5,
        blank=True, null=True,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
        ],
        verbose_name=_("Blood Group")
    )
    # Medical History (Antécédents médicaux)
    medical_history = models.TextField(
        blank=True, null=True,
        help_text=_("E.g., allergies, chronic diseases"),
        verbose_name=_("Medical History (Allergies, Chronic Diseases)")
    )

    # Identification Numbers
    patient_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Patient ID")
    )
    social_security_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True, null=True,
        verbose_name=_("Social Security Number")
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, verbose_name=_("Emergency Contact Name"))
    emergency_contact_phone = models.CharField(max_length=20, verbose_name=_("Emergency Contact Phone"))
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Emergency Contact Relationship"))

    date_registered = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Registered"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        ordering = ['last_name', 'first_name']
