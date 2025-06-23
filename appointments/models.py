# Create your models here.
from django.db import models
from patients.models import Patient
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    """
    Manages patient appointments.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_("Patient")
    )
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'user_type': 'doctor'},
        related_name='doctor_appointments',
        verbose_name=_("Doctor")
    )
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    reason = models.TextField(verbose_name=_("Reason for Appointment"))
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('rescheduled', 'Rescheduled')
        ],
        default='scheduled',
        verbose_name=_("Status")
    )
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    def __str__(self):
        return f"Appointment for {self.patient.first_name} {self.patient.last_name} with Dr. {self.doctor.last_name} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        ordering = ['start_time']
        # Ensure no overlapping appointments for the same doctor at the same time
        unique_together = ('doctor', 'start_time', 'end_time')
