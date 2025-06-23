from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import role_required
from .models import Appointment
from .forms import AppointmentForm, PatientAppointmentForm

def home(request):
    return render(request, "home.html")

@login_required
@role_required(['patient', 'doctor', 'admin'])
def appointment_list(request):
    """Show appointments based on user role."""
    user = request.user
    
    if user.user_type == 'patient':
        # Patients can only see their own appointments
        try:
            patient_profile = user.patient_profile
            appointments = Appointment.objects.filter(patient=patient_profile)
        except AttributeError:
            messages.error(request, "Your user profile is not linked to a patient profile.")
            appointments = Appointment.objects.none()

        context = {
            'appointments': appointments,
            'user_role': 'patient',
            'title': 'My Appointments'
        }
    elif user.user_type in ['doctor', 'admin']:
        # Doctors and admins can see all appointments
        appointments = Appointment.objects.all()
        context = {
            'appointments': appointments,
            'user_role': user.user_type,
            'title': 'All Appointments'
        }
    else:
        messages.error(request, "Access denied.")
        return redirect('core:dashboard')
    
    return render(request, 'appointments/appointment_list.html', context)

@login_required
@role_required(['patient', 'doctor', 'admin'])
def appointment_create(request):
    """Create new appointment with role-based restrictions."""
    user = request.user
    if user.user_type == 'patient':
        try:
            patient_profile = user.patient_profile
        except AttributeError:
            messages.error(request, "Your user profile is not linked to a patient profile.")
            return redirect('core:dashboard')
        if request.method == 'POST':
            form = PatientAppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = patient_profile
                appointment.status = 'scheduled'
                appointment.save()
                messages.success(request, "Appointment request submitted successfully!")
                return redirect('appointments:appointment_list')
        else:
            form = PatientAppointmentForm()
        context = {
            'form': form,
            'title': 'Request Appointment'
        }
        return render(request, 'appointments/appointment_form.html', context)
    else:
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Appointment created successfully!")
                return redirect('appointments:appointment_list')
        else:
            form = AppointmentForm()
            # Pre-fill doctor if the user is a doctor
            if user.user_type == 'doctor':
                form.fields['doctor'].initial = user
        context = {
            'form': form,
            'title': 'Create Appointment'
        }
        return render(request, 'appointments/appointment_form.html', context)

@login_required
@role_required(['patient', 'doctor', 'admin'])
def appointment_detail(request, pk):
    """Show appointment details with role-based access."""
    user = request.user
    
    if user.user_type == 'patient':
        # Patients can only see their own appointments
        try:
            patient_profile = user.patient_profile
            appointment = get_object_or_404(Appointment, pk=pk, patient=patient_profile)
        except AttributeError:
            messages.error(request, "Your user profile is not linked to a patient profile.")
            return redirect('core:dashboard')
    elif user.user_type in ['doctor', 'admin']:
        # Doctors and admins can see any appointment
        appointment = get_object_or_404(Appointment, pk=pk)
    else:
        messages.error(request, "Access denied.")
        return redirect('core:dashboard')
    
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
@role_required(['patient', 'doctor', 'admin'])
def appointment_update(request, pk):
    """Update appointment with role-based restrictions."""
    user = request.user
    
    if user.user_type == 'patient':
        # Patients can only update their own appointments
        try:
            patient_profile = user.patient_profile
            appointment = get_object_or_404(Appointment, pk=pk, patient=patient_profile)
        except AttributeError:
            messages.error(request, "Your user profile is not linked to a patient profile.")
            return redirect('core:dashboard')
    elif user.user_type in ['doctor', 'admin']:
        # Doctors and admins can update any appointment
        appointment = get_object_or_404(Appointment, pk=pk)
    else:
        messages.error(request, "Access denied.")
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, "Appointment updated successfully!")
        return redirect('appointments:appointment_detail', pk=appointment.pk)
    
    return render(request, 'appointments/appointment_form.html', {'appointment': appointment})

@login_required
@role_required(['patient', 'doctor', 'admin'])
def appointment_delete(request, pk):
    """Delete appointment with role-based restrictions."""
    user = request.user
    
    if user.user_type == 'patient':
        # Patients can only delete their own appointments
        try:
            patient_profile = user.patient_profile
            appointment = get_object_or_404(Appointment, pk=pk, patient=patient_profile)
        except AttributeError:
            messages.error(request, "Your user profile is not linked to a patient profile.")
            return redirect('core:dashboard')
    elif user.user_type in ['doctor', 'admin']:
        # Doctors and admins can delete any appointment
        appointment = get_object_or_404(Appointment, pk=pk)
    else:
        messages.error(request, "Access denied.")
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
        return redirect('appointments:appointment_list')
    
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})