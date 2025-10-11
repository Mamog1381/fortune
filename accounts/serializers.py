from rest_framework import serializers
from django.conf import settings
import re


class SendOTPSerializer(serializers.Serializer):
    """Serializer for sending OTP"""
    phone_number = serializers.CharField(
        max_length=15,
        required=True,
        help_text="Phone number to send OTP to"
    )

    def validate_phone_number(self, value):
        """Validate phone number format"""
        # Remove any spaces or special characters
        phone_number = re.sub(r'[^\d+]', '', value)

        # Basic validation - adjust based on your requirements
        if not phone_number:
            raise serializers.ValidationError("Invalid phone number format")

        if len(phone_number) < 10:
            raise serializers.ValidationError("Phone number too short")

        return phone_number


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying OTP"""
    phone_number = serializers.CharField(
        max_length=15,
        required=True,
        help_text="Phone number that received the OTP"
    )
    otp_code = serializers.CharField(
        max_length=settings.OTP_LENGTH,
        min_length=settings.OTP_LENGTH,
        required=True,
        help_text="OTP code received via SMS"
    )

    def validate_phone_number(self, value):
        """Validate phone number format"""
        phone_number = re.sub(r'[^\d+]', '', value)

        if not phone_number:
            raise serializers.ValidationError("Invalid phone number format")

        return phone_number

    def validate_otp_code(self, value):
        """Validate OTP code format"""
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits")

        return value


class UserSerializer(serializers.Serializer):
    """Serializer for user information"""
    id = serializers.IntegerField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
