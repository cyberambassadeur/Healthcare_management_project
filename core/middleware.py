# healthcare_system/core/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import logging

# Set up logger
logger = logging.getLogger('core.middleware')

class UserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = request.user

        # Define paths that are ALWAYS accessible, regardless of authentication status.
        # These are truly public paths that AnonymousUser can access.
        allowed_public_paths = (
            '/admin/login/',      # Admin login page
            '/accounts/login/',   # Your custom accounts login page
            '/accounts/register/', # Registration page
            '/accounts/password_reset/', # Password reset
            '/api/',              # All API endpoints
            '/',                  # The homepage/landing page
            '/static/',           # Important for CSS/JS files
            '/media/',            # Important for user-uploaded media files
        )

        # Check if the current path is one of the explicitly allowed public paths.
        if any(path.startswith(p) for p in allowed_public_paths):
            # If it's a public path, let the request proceed immediately.
            return self.get_response(request)

        # If we reach here, the path is NOT explicitly public.
        # Now, we must ensure the user IS authenticated to proceed.

        # If the user is NOT authenticated at this point, they are trying to access a protected page.
        if not user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt to {path}")
            messages.error(request, "Please log in to access this page.")
            return redirect('users:login')

        # If we reach here, it means:
        # 1. The path is NOT a publicly allowed path.
        # 2. The user IS authenticated.
        # Now, and ONLY now, it is safe to check user.user_type for role-based access.

        # Define role-specific access rules
        if user.user_type == 'patient':
            # Patients can only access patient-specific areas
            allowed_patient_paths = (
                '/dashboard/',           # Patient dashboard
                '/patients/',            # Patient-specific features
                '/appointments/',        # Patient appointments
                '/accounts/',            # Account management
                '/accounts/logout/',     # Logout
            )
            
            # Check if patient is trying to access doctor/admin areas
            restricted_paths = (
                '/doctors/',             # Doctor management
                '/medical-records/',     # Medical records (doctors only)
                '/admin/',               # Admin panel
            )
            
            if any(path.startswith(p) for p in restricted_paths):
                logger.warning(f"Patient {user.username} attempted to access restricted area: {path}")
                messages.error(request, "Access denied. Patients cannot access this area.")
                return redirect('core:dashboard')
                
            if not any(path.startswith(p) for p in allowed_patient_paths):
                logger.info(f"Patient {user.username} redirected to dashboard from: {path}")
                messages.warning(request, "Redirecting to your dashboard.")
                return redirect('core:dashboard')
                
        elif user.user_type == 'doctor':
            # Doctors can access doctor-specific areas
            allowed_doctor_paths = (
                '/dashboard/',           # Doctor dashboard
                '/patients/',            # Patient management
                '/appointments/',        # Appointment management
                '/medical-records/',     # Medical records
                '/accounts/',            # Account management
                '/accounts/logout/',     # Logout
            )
            
            # Check if doctor is trying to access admin areas
            restricted_paths = (
                '/admin/',               # Admin panel (unless they're also admin)
            )
            
            if any(path.startswith(p) for p in restricted_paths) and not user.is_superuser:
                logger.warning(f"Doctor {user.username} attempted to access admin area: {path}")
                messages.error(request, "Access denied. Doctors cannot access admin areas.")
                return redirect('core:dashboard')
                
            if not any(path.startswith(p) for p in allowed_doctor_paths):
                logger.info(f"Doctor {user.username} redirected to dashboard from: {path}")
                messages.warning(request, "Redirecting to your dashboard.")
                return redirect('core:dashboard')
                
        elif user.user_type == 'admin':
            # Admins have full access to everything
            logger.info(f"Admin {user.username} accessed: {path}")
            pass
        elif user.user_type == 'staff':
            # Staff can access limited areas
            allowed_staff_paths = (
                '/dashboard/',           # Staff dashboard
                '/appointments/',        # Appointment management
                '/accounts/',            # Account management
                '/accounts/logout/',     # Logout
            )
            
            if not any(path.startswith(p) for p in allowed_staff_paths):
                logger.info(f"Staff {user.username} redirected to dashboard from: {path}")
                messages.warning(request, "Redirecting to your dashboard.")
                return redirect('core:dashboard')
        else:
            # Handle cases for authenticated users with unexpected or undefined user_type.
            logger.error(f"User {user.username} has invalid user_type: {user.user_type}")
            messages.error(request, "Invalid user type. Please contact support.")
            return redirect('users:login')

        # If the request hasn't been returned by now, allow it to proceed.
        response = self.get_response(request)
        return response