from django import forms
from .models import Patient
from django.core.exceptions import ValidationError
from datetime import date

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'address',
            'phone_number', 'email', 'blood_group', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob 