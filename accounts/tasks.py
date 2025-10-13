from celery import shared_task
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_otp_sms(self, phone_number: str, otp_code: str):
    """
    Celery task to send OTP via SMS

    Args:
        phone_number: Recipient phone number
        otp_code: OTP code to send

    Returns:
        Dict with success status and message

    Raises:
        Retries the task on failure with exponential backoff
    """
    try:
        logger.info(f"Sending OTP to {phone_number}")

        # For development/testing, just log the OTP
        if settings.DEBUG:
            logger.info(f"[DEBUG MODE] OTP for {phone_number}: {otp_code}")
            print(f"\n{'='*50}")
            print(f"[DEBUG MODE] OTP CODE")
            print(f"Phone: {phone_number}")
            print(f"Code: {otp_code}")
            print(f"{'='*50}\n")
            return {
                'success': True,
                'phone_number': phone_number,
                'message': 'OTP logged (DEBUG mode)',
                'debug': True
            }

        # Production: Use configured SMS provider
        from .sms_providers import get_sms_provider

        provider = get_sms_provider()

        # Check if provider is configured
        if not provider.is_configured():
            logger.warning("SMS provider is not configured. OTP will only be logged.")
            logger.info(f"[PRODUCTION - NO SMS CONFIG] OTP for {phone_number}: {otp_code}")
            return {
                'success': False,
                'phone_number': phone_number,
                'message': 'SMS provider not configured',
                'otp_code': otp_code  # Only in logs, not sent to client
            }

        # Send OTP via SMS provider
        result = provider.send_otp(phone_number, otp_code)

        if result['success']:
            logger.info(f"OTP sent successfully to {phone_number}")
            return {
                'success': True,
                'phone_number': phone_number,
                'message': 'OTP sent successfully'
            }
        else:
            # Log failure but don't retry if it's a provider-specific error
            logger.error(f"SMS provider failed to send OTP to {phone_number}: {result['message']}")
            return {
                'success': False,
                'phone_number': phone_number,
                'message': result['message']
            }

    except Exception as exc:
        logger.error(f"Failed to send OTP to {phone_number}: {str(exc)}")

        # Retry the task with exponential backoff
        # Max 3 retries with 60s, 120s, 180s delays
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
