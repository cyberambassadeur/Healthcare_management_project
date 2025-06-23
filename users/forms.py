# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser # Import your custom user model

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users based on CustomUser model.
    Extends Django's UserCreationForm.
    """
    class Meta:
        model = CustomUser
        # Explicitly list all fields you want in the registration form.
        # UserCreationForm already provides username and password fields implicitly.
        # We add email, user_type, first_name, last_name.
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for changing existing users in the admin.
    Extends Django's UserChangeForm.
    """
    class Meta:
        model = CustomUser
        # Explicitly list all fields for changing users, including inherited ones.
        # This is more robust than trying to concatenate with UserChangeForm.Meta.fields
        fields = (
            'username',
            'email',
            'user_type',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )

# Example: If you need a separate form for user login (not always necessary
# if using default Django login views, but good for custom scenarios):
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class DoctorProfileForm(forms.ModelForm):
    """
    Form for doctors to edit their own profile information.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class PatientSetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, help_text="Enter the username given by your doctor.")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data