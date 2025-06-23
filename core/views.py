from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from patients.models import Patient
from medical_records.models import LabResult, Prescription, MedicalRecord

# Create your views here.
# core/views.py
from django.shortcuts import render
from django.http import HttpResponse # Import HttpResponse for a simple text response
import datetime

def home_view(request):
    """
    View for the home page with login and registration forms.
    """
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    """
    Dashboard view for authenticated users with role-based access control.
    """
    user = request.user
    
    # Additional security check - ensure user has a valid user_type
    if not hasattr(user, 'user_type') or not user.user_type:
        raise PermissionDenied("Invalid user account. Please contact support.")
    
    # Role-based context
    context = {
        'user': user,
        'is_patient': user.is_patient,
        'is_doctor': user.is_doctor,
        'is_admin': user.is_admin_user,
        'is_staff': user.is_staff_user,
    }

    if user.is_patient:
        try:
            patient_profile = user.patient_profile
            from appointments.models import Appointment
            from medical_records.models import MedicalRecord
            from django.utils import timezone

            context['upcoming_appointments_count'] = Appointment.objects.filter(
                patient=patient_profile,
                start_time__gte=timezone.now()
            ).count()
            context['medical_records_count'] = MedicalRecord.objects.filter(patient=patient_profile).count()
        except AttributeError:
            context['upcoming_appointments_count'] = 0
            context['medical_records_count'] = 0

    if user.is_doctor:
        from appointments.models import Appointment
        from django.utils import timezone
        today = timezone.now().date()
        
        context['todays_patients_count'] = Appointment.objects.filter(
            doctor=user,
            start_time__date=today
        ).count()
        context['pending_appointments_count'] = Appointment.objects.filter(
            doctor=user,
            status='scheduled'
        ).count()

    # Log access for security monitoring
    print(f"Dashboard accessed by {user.username} (Type: {user.user_type})")
    
    return render(request, 'core/dashboard.html', context)

@login_required
def patient_profile_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'patients/view_profile.html', {'patient': patient})

@login_required
def patient_record_list(request):
    patient = get_object_or_404(Patient, user=request.user)
    record_type = request.GET.get('type')
    if record_type == 'lab':
        records = LabResult.objects.filter(medical_record__patient=patient)
        template = 'medical_records/lab_results_list.html'
    elif record_type == 'prescription':
        records = Prescription.objects.filter(medical_record__patient=patient)
        template = 'medical_records/prescriptions_list.html'
    else:
        records = MedicalRecord.objects.filter(patient=patient)
        template = 'medical_records/record_list.html'
    return render(request, template, {'records': records})

def create_appointment(request):
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Set time to 09:00 by default
            date_only = form.cleaned_data['start_time']
            appointment.start_time = datetime.datetime.combine(date_only, datetime.time(9, 0))
            appointment.patient = request.user.patient_profile
            appointment.save()
            # ... redirect or show success

# You can add more views here later
