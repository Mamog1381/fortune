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
    """
    try:
        # TODO: Integrate with your SMS provider
        # Example integration points:
        # - Twilio
        # - AWS SNS
        # - Custom SMS gateway

        logger.info(f"Sending OTP {otp_code} to {phone_number}")

        # Placeholder for SMS sending logic
        # Replace this with actual SMS provider integration
        message = f"Your Coffee Fortune verification code is: {otp_code}"

        # Example: Twilio integration (uncomment when configured)
        # from twilio.rest import Client
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(
        #     body=message,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=phone_number
        # )

        # For development/testing, just log the OTP
        if settings.DEBUG:
            logger.info(f"[DEBUG MODE] OTP for {phone_number}: {otp_code}")
            print(f"[DEBUG MODE] OTP for {phone_number}: {otp_code}")

        return {
            'success': True,
            'phone_number': phone_number,
            'message': 'OTP sent successfully'
        }

    except Exception as exc:
        logger.error(f"Failed to send OTP to {phone_number}: {str(exc)}")

        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
