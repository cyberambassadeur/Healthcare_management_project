# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required # For protecting views
from django.contrib import messages # For displaying success/error messages
from django.views.generic import CreateView # For class-based registration view
from django.urls import reverse_lazy # For redirecting after successful form submission
from django.contrib.auth.views import LogoutView

from .forms import CustomUserCreationForm, DoctorProfileForm, PatientSetPasswordForm # Import your custom registration form
from .models import CustomUser # Import your CustomUser model
from core.decorators import role_required

class RegisterView(CreateView):
    """
    Class-based view for user registration.
    Uses CustomUserCreationForm to create new users.
    """
    form_class = CustomUserCreationForm
    template_name = 'users/register.html' # We will create this template next
    success_url = reverse_lazy('users:login') # Redirect to login page after successful registration

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating account. Please check the form.')
        return super().form_invalid(form)


def user_login(request):
    """
    View for user login.
    Handles both GET (display form) and POST (process form) requests.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to a dashboard or home page after login
            return redirect('core:home') # Make sure 'core:home' is defined in core/urls.py
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html') # Default Django login template path

@login_required
def user_logout(request):
    """
    Custom logout view that accepts GET requests.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login') # Redirect to login page after logout

@login_required
def user_dashboard(request):
    """
    A simple dashboard view for authenticated users.
    This will be customized later based on user type.
    """
    return render(request, 'users/dashboard.html', {'user': request.user})

@login_required
@role_required(['doctor'])
def edit_doctor_profile(request):
    """
    Allow a doctor to edit their own profile.
    """
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:edit-doctor-profile')
    else:
        form = DoctorProfileForm(instance=request.user)

    context = {
        'form': form,
        'title': 'Edit My Profile'
    }
    return render(request, 'users/edit_doctor_profile.html', context)

def patient_register(request):
    """
    Allow a patient to set a password for an existing user (created by the doctor, with no password).
    """
    if request.method == 'POST':
        form = PatientSetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                user = CustomUser.objects.get(username=username, user_type='patient')
            except CustomUser.DoesNotExist:
                form.add_error('username', 'No patient account with this username. Please get your username from your doctor.')
            else:
                if user.has_usable_password():
                    form.add_error('username', 'This account is already registered. Please log in or reset your password.')
                else:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Account activated! You can now log in.')
                    return redirect('users:login')
    else:
        form = PatientSetPasswordForm()
    return render(request, 'users/patient_register.html', {'form': form})
