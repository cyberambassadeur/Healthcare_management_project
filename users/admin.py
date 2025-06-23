# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Import Django's default UserAdmin
from .models import CustomUser # Import your custom user model
from .forms import CustomUserCreationForm, CustomUserChangeForm # Import your custom forms

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff') # Changed 'role' to 'user_type'
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups') # Changed 'role' to 'user_type'
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Define custom fieldsets for the admin change form
    fieldsets = UserAdmin.fieldsets + (
        (('User Type'), {'fields': ('user_type',)}), # Added user_type to fieldsets
    )
    # Define custom add_fieldsets for the admin add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('User Type'), {'fields': ('user_type',)}), # Added user_type to add_fieldsets
    )