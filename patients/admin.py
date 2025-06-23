# Register your models here.
from django.contrib import admin
from .models import Patient
from django.utils.translation import gettext_lazy as _

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'phone_number', 'email', 'date_of_birth', 'gender', 'date_registered')
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone_number', 'email', 'social_security_number')
    list_filter = ('gender', 'blood_group', 'date_registered')
    readonly_fields = ('patient_id', 'date_registered', 'last_updated')
    fieldsets = (
        (_("Patient Profile"), {
            'fields': ('user', ('first_name', 'last_name'), ('date_of_birth', 'gender'), 'address', ('phone_number', 'email'), ('patient_id', 'social_security_number'))
        }),
        (_("Medical Details"), {
            'fields': ('blood_group', 'medical_history')
        }),
        (_("Emergency Contact"), {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        (_("Timestamps"), {
            'fields': ('date_registered', 'last_updated'),
            'classes': ('collapse',) # Collapse this section in admin
        }),
    )
