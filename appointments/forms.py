from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'start_time', 'end_time', 'reason', 'status', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
            raise ValidationError("Appointment start time cannot be in the past.")
        return start_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise ValidationError("End time must be after start time.")

        return cleaned_data

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.input_type = 'date'
        self.fields['start_time'].label = "Date" 