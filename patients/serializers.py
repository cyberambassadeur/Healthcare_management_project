# patients/serializers.py
from rest_framework import serializers
from .models import Patient
from users.models import CustomUser # Import CustomUser
from users.serializers import CustomUserSerializer
from datetime import date

# Serializer for the CustomUser model (used for Patient's user field)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type']
        read_only_fields = ['user_type'] # User type should not be directly updated via patient profile API

class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = CustomUser.objects.create(**user_data)
            validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'patient_id', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'address', 'phone_number', 'email', 'blood_group',
            'medical_history', 'social_security_number',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'date_registered', 'last_updated'
        ]
        read_only_fields = ['patient_id', 'date_registered', 'last_updated'] # These are auto-generated