from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role.
    
    Usage:
    @role_required(['doctor', 'admin'])
    def doctor_only_view(request):
        return render(request, 'doctor_view.html')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('users:login')
            
            if not hasattr(request.user, 'user_type'):
                messages.error(request, "Invalid user account. Please contact support.")
                return redirect('users:login')
            
            if request.user.user_type not in allowed_roles:
                messages.error(request, f"Access denied. This area is restricted to {', '.join(allowed_roles)}.")
                return redirect('core:dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def patient_only(view_func):
    """Decorator to restrict access to patients only."""
    return role_required(['patient'])(view_func)

def doctor_only(view_func):
    """Decorator to restrict access to doctors only."""
    return role_required(['doctor'])(view_func)

def admin_only(view_func):
    """Decorator to restrict access to admins only."""
    return role_required(['admin'])(view_func)

def staff_only(view_func):
    """Decorator to restrict access to staff only."""
    return role_required(['staff'])(view_func) 