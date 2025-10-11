from django.core.cache import cache
from django.conf import settings
from rest_framework.exceptions import Throttled
from typing import Optional


class RedisProtection:
    """Redis-based protection against brute-force attacks"""

    @staticmethod
    def get_otp_attempt_key(phone_number: str) -> str:
        """Generate cache key for OTP attempts"""
        return f'otp_attempt:{phone_number}'

    @staticmethod
    def get_otp_block_key(phone_number: str) -> str:
        """Generate cache key for blocked phone numbers"""
        return f'otp_blocked:{phone_number}'

    @staticmethod
    def get_otp_code_key(phone_number: str) -> str:
        """Generate cache key for OTP code"""
        return f'otp_code:{phone_number}'

    @staticmethod
    def is_blocked(phone_number: str) -> bool:
        """Check if phone number is blocked"""
        block_key = RedisProtection.get_otp_block_key(phone_number)
        return cache.get(block_key) is not None

    @staticmethod
    def block_phone_number(phone_number: str, duration: Optional[int] = None):
        """Block phone number for specified duration"""
        if duration is None:
            duration = settings.OTP_BLOCK_DURATION

        block_key = RedisProtection.get_otp_block_key(phone_number)
        cache.set(block_key, True, duration)

    @staticmethod
    def increment_attempt(phone_number: str) -> int:
        """Increment failed OTP attempts and return current count"""
        attempt_key = RedisProtection.get_otp_attempt_key(phone_number)

        attempts = cache.get(attempt_key, 0)
        attempts += 1

        # Store attempts for OTP_BLOCK_DURATION
        cache.set(attempt_key, attempts, settings.OTP_BLOCK_DURATION)

        return attempts

    @staticmethod
    def reset_attempts(phone_number: str):
        """Reset failed OTP attempts"""
        attempt_key = RedisProtection.get_otp_attempt_key(phone_number)
        cache.delete(attempt_key)

    @staticmethod
    def get_attempts(phone_number: str) -> int:
        """Get current number of failed attempts"""
        attempt_key = RedisProtection.get_otp_attempt_key(phone_number)
        return cache.get(attempt_key, 0)

    @staticmethod
    def check_and_enforce(phone_number: str):
        """Check if phone number is blocked and raise exception if needed"""
        if RedisProtection.is_blocked(phone_number):
            raise Throttled(
                detail="Too many failed attempts. Please try again later."
            )

        attempts = RedisProtection.get_attempts(phone_number)
        if attempts >= settings.MAX_OTP_ATTEMPTS:
            RedisProtection.block_phone_number(phone_number)
            raise Throttled(
                detail="Too many failed attempts. Your phone number has been temporarily blocked."
            )

    @staticmethod
    def store_otp(phone_number: str, otp_code: str):
        """Store OTP code in cache"""
        otp_key = RedisProtection.get_otp_code_key(phone_number)
        cache.set(otp_key, otp_code, settings.OTP_EXPIRY_SECONDS)

    @staticmethod
    def get_otp(phone_number: str) -> Optional[str]:
        """Retrieve OTP code from cache"""
        otp_key = RedisProtection.get_otp_code_key(phone_number)
        return cache.get(otp_key)

    @staticmethod
    def delete_otp(phone_number: str):
        """Delete OTP code from cache"""
        otp_key = RedisProtection.get_otp_code_key(phone_number)
        cache.delete(otp_key)

    @staticmethod
    def get_send_otp_rate_limit_key(phone_number: str) -> str:
        """Generate cache key for OTP send rate limiting"""
        return f'otp_send_limit:{phone_number}'

    @staticmethod
    def can_send_otp(phone_number: str) -> bool:
        """Check if OTP can be sent (rate limiting)"""
        rate_limit_key = RedisProtection.get_send_otp_rate_limit_key(phone_number)
        return cache.get(rate_limit_key) is None

    @staticmethod
    def set_send_otp_limit(phone_number: str, duration: int = 60):
        """Set rate limit for sending OTP"""
        rate_limit_key = RedisProtection.get_send_otp_rate_limit_key(phone_number)
        cache.set(rate_limit_key, True, duration)
