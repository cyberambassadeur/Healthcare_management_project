# users/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Define user type choices
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
        ('staff', 'Staff'), # Example: for receptionists, nurses
    )
    user_type = models.CharField(
        _("User Type"),
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='patient', # Default user type for new registrations (overridden for superusers)
        help_text=_("Designates the type of user (e.g., Patient, Doctor, Admin).")
    )

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set", # Unique related_name
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set", # Unique related_name
        related_query_name="customuser",
    )

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")

    def __str__(self):
        return self.username

    # --- NEW CODE ADDED HERE ---
    # Override the save method to ensure superusers always have user_type='admin'
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = 'admin'
        super().save(*args, **kwargs)
    # --- END NEW CODE ---

    @property
    def is_patient(self):
        return self.user_type == 'patient'

    @property
    def is_doctor(self):
        return self.user_type == 'doctor'

    @property
    def is_admin_user(self):
        return self.user_type == 'admin'

    @property
    def is_staff_user(self):
        return self.user_type == 'staff'