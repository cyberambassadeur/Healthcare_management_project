# users/urls.py

from django.urls import path
from . import views # Import the views you just created
from django.contrib.auth import views as auth_views # Import Django's built-in auth views for login/logout (optional, but good for defaults)

app_name = 'users' # This is good practice for namespacing your app's URLs

urlpatterns = [
    # User Registration
    path('register/', views.RegisterView.as_view(), name='register'),
    path('patient-register/', views.patient_register, name='patient-register'),

    # User Login
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
        next_page='core:dashboard'
    ), name='login'),

    # User Logout - Using custom view that accepts GET requests
    path('logout/', views.user_logout, name='logout'),

    # User Dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),

    # Doctor Profile Edit
    path('profile/edit/', views.edit_doctor_profile, name='edit-doctor-profile'),

    # Password Reset URLs - Using Django's default URL names
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/accounts/password_reset/done/'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]