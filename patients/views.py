from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from users.models import CustomUser
from .serializers import PatientSerializer
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from .forms import PatientForm
from django.contrib import messages

# Create your views here.
# patients/views.py

# Basic Django view (if you have one, keep it or remove if only API)
def home(request):
    return render(request, 'patients/home.html') # Assuming you have a home.html in patients/templates

# API ViewSet for Patient model
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# API views for REST endpoints
@api_view(['GET'])
def patient_list_api(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def patient_detail_api(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    serializer = PatientSerializer(patient)
    return Response(serializer.data)

@login_required
@role_required(['patient'])
def edit_patient_profile(request):
    """
    Allow a patient to edit their own profile.
    """
    try:
        patient_profile = request.user.patient_profile
    except CustomUser.patient_profile.RelatedObjectDoesNotExist:
        messages.error(request, "Could not find a patient profile associated with your account.")
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('patients:edit-profile')
    else:
        form = PatientForm(instance=patient_profile)

    context = {
        'form': form,
        'title': 'Edit My Profile'
    }
    return render(request, 'patients/edit_profile.html', context)

@login_required
@role_required(['doctor', 'admin'])
def patient_list(request):
    """
    Display a list of all patients for doctors and admins.
    """
    patients = Patient.objects.all()
    context = {
        'patients': patients,
        'title': 'Patient List'
    }
    return render(request, 'patients/patient_list.html', context)

@login_required
def patient_profile_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'patients/view_profile.html', {'patient': patient})
