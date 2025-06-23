# Register your models here.
from django.contrib import admin
from .models import Appointment
from django.utils.translation import gettext_lazy as _

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'start_time', 'end_time', 'status', 'reason')
    list_filter = ('status', 'doctor', 'start_time')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason')
    raw_id_fields = ('patient', 'doctor') # Use raw_id_fields for FKs
    fieldsets = (
        (None, {'fields': ('patient', 'doctor', ('start_time', 'end_time'), 'status', 'reason')}),
        (_("Additional Information"), {'fields': ('notes',)}),
        (_("Timestamps"), {
            'fields': ('date_created', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_created', 'last_updated')
