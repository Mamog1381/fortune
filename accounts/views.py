from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import User
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserSerializer
from .redis_protection import RedisProtection
from .tasks import send_otp_sms

import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    """
    Send OTP to phone number

    Request Body:
        phone_number (str): Phone number to send OTP to

    Returns:
        200: OTP sent successfully
        400: Invalid phone number or validation error
        429: Rate limit exceeded
    """
    serializer = SendOTPSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    phone_number = serializer.validated_data['phone_number']

    # Check if phone number is blocked
    try:
        RedisProtection.check_and_enforce(phone_number)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Check rate limiting for sending OTP
    if not RedisProtection.can_send_otp(phone_number):
        return Response(
            {'error': 'Please wait before requesting another OTP'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Generate OTP
    otp_code = get_random_string(
        length=settings.OTP_LENGTH,
        allowed_chars='0123456789'
    )

    # Store OTP in Redis
    RedisProtection.store_otp(phone_number, otp_code)

    # Set rate limit for sending OTP (60 seconds)
    RedisProtection.set_send_otp_limit(phone_number, duration=60)

    # Send OTP via Celery task
    send_otp_sms.delay(phone_number, otp_code)

    logger.info(f"OTP requested for phone number: {phone_number}")

    return Response(
        {
            'message': 'OTP sent successfully',
            'phone_number': phone_number,
            'expires_in': settings.OTP_EXPIRY_SECONDS
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verify OTP and authenticate user

    Request Body:
        phone_number (str): Phone number
        otp_code (str): OTP code received

    Returns:
        200: OTP verified, returns JWT tokens
        400: Invalid OTP or validation error
        429: Too many failed attempts
    """
    serializer = VerifyOTPSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    phone_number = serializer.validated_data['phone_number']
    otp_code = serializer.validated_data['otp_code']

    # Check if phone number is blocked
    try:
        RedisProtection.check_and_enforce(phone_number)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Get stored OTP from Redis
    stored_otp = RedisProtection.get_otp(phone_number)

    if not stored_otp:
        return Response(
            {'error': 'OTP expired or not found. Please request a new one.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify OTP
    if stored_otp != otp_code:
        # Increment failed attempts
        attempts = RedisProtection.increment_attempt(phone_number)

        remaining_attempts = settings.MAX_OTP_ATTEMPTS - attempts

        if remaining_attempts <= 0:
            RedisProtection.block_phone_number(phone_number)
            return Response(
                {'error': 'Too many failed attempts. Your phone number has been temporarily blocked.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {
                'error': 'Invalid OTP code',
                'remaining_attempts': remaining_attempts
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # OTP is valid - reset attempts and delete OTP
    RedisProtection.reset_attempts(phone_number)
    RedisProtection.delete_otp(phone_number)

    # Get or create user
    user, created = User.objects.get_or_create(phone_number=phone_number)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    logger.info(f"User authenticated: {phone_number} (created: {created})")

    return Response(
        {
            'message': 'Authentication successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        },
        status=status.HTTP_200_OK
    )
