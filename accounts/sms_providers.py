"""
SMS Provider Integration
Support for various SMS providers including Faraz SMS (Iranian provider)
"""

import requests
import logging
from typing import Dict, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class FarazSMSProvider:
    """
    Faraz SMS Provider Integration (https://farazsms.com)

    این کلاس برای ارسال پیامک از طریق پنل فراز پیامک است.
    دو روش ارسال دارد:
    1. ارسال الگو محور (Pattern) - برای OTP (توصیه می‌شود)
    2. ارسال ساده (Simple) - برای پیامک‌های عادی
    """

    BASE_URL = "https://api2.ippanel.com"

    def __init__(self):
        """
        Initialize Faraz SMS Provider

        Required settings:
            FARAZ_API_KEY: Your API key from Faraz panel
            FARAZ_ORIGINATOR: Your originator number (10-digit number)
            FARAZ_PATTERN_CODE: Pattern code for OTP (optional, for pattern-based sending)
        """
        self.api_key = getattr(settings, 'FARAZ_API_KEY', '')
        self.originator = getattr(settings, 'FARAZ_ORIGINATOR', '')
        self.pattern_code = getattr(settings, 'FARAZ_PATTERN_CODE', '')

        if not self.api_key:
            logger.warning("FARAZ_API_KEY is not configured")

        if not self.originator:
            logger.warning("FARAZ_ORIGINATOR is not configured")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }

    def send_pattern(
        self,
        phone_number: str,
        pattern_values: Dict[str, str],
        pattern_code: Optional[str] = None
    ) -> Dict[str, any]:
        """
        ارسال پیامک الگو محور (Pattern-based SMS)

        این روش برای ارسال OTP توصیه می‌شود چون سریع‌تر و ارزان‌تر است.

        Args:
            phone_number: شماره موبایل گیرنده (با 98 یا بدون)
            pattern_values: مقادیر متغیرهای الگو (مثلا {"code": "123456"})
            pattern_code: کد الگو (اختیاری، اگر ندید از تنظیمات می‌خواند)

        Returns:
            Dict with 'success', 'message', and 'data' keys

        Example:
            >>> provider = FarazSMSProvider()
            >>> result = provider.send_pattern(
            ...     phone_number="09123456789",
            ...     pattern_values={"code": "123456"}
            ... )
        """
        try:
            # Normalize phone number
            phone = self._normalize_phone(phone_number)

            # Use provided pattern code or default from settings
            code = pattern_code or self.pattern_code

            if not code:
                raise ValueError("Pattern code is required. Set FARAZ_PATTERN_CODE in settings or provide pattern_code parameter.")

            url = f"{self.BASE_URL}/api/v1/sms/pattern/normal/send"

            payload = {
                "code": code,
                "sender": self.originator,
                "recipient": phone,
                "variable": pattern_values
            }

            logger.info(f"Sending pattern SMS to {phone} with pattern {code}")

            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )

            response_data = response.json()

            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Pattern SMS sent successfully to {phone}")
                return {
                    'success': True,
                    'message': 'SMS sent successfully',
                    'data': response_data
                }
            else:
                logger.error(f"Failed to send pattern SMS: {response_data}")
                return {
                    'success': False,
                    'message': f"SMS sending failed: {response_data.get('message', 'Unknown error')}",
                    'data': response_data
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout sending SMS to {phone_number}")
            return {
                'success': False,
                'message': 'SMS sending timeout',
                'data': None
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error sending SMS to {phone_number}: {str(e)}")
            return {
                'success': False,
                'message': f'SMS sending error: {str(e)}',
                'data': None
            }

        except Exception as e:
            logger.error(f"Unexpected error sending pattern SMS to {phone_number}: {str(e)}")
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}',
                'data': None
            }

    def send_simple(
        self,
        phone_numbers: list[str],
        message: str
    ) -> Dict[str, any]:
        """
        ارسال پیامک ساده (Simple SMS)

        برای ارسال پیامک‌های متنی عادی استفاده می‌شود.

        Args:
            phone_numbers: لیست شماره موبایل گیرندگان
            message: متن پیامک

        Returns:
            Dict with 'success', 'message', and 'data' keys

        Example:
            >>> provider = FarazSMSProvider()
            >>> result = provider.send_simple(
            ...     phone_numbers=["09123456789"],
            ...     message="کد تایید شما: 123456"
            ... )
        """
        try:
            # Normalize phone numbers
            phones = [self._normalize_phone(phone) for phone in phone_numbers]

            url = f"{self.BASE_URL}/api/v1/sms/send/webservice/single"

            payload = {
                "sender": self.originator,
                "recipient": phones,
                "message": message
            }

            logger.info(f"Sending simple SMS to {len(phones)} recipients")

            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )

            response_data = response.json()

            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Simple SMS sent successfully to {len(phones)} recipients")
                return {
                    'success': True,
                    'message': 'SMS sent successfully',
                    'data': response_data
                }
            else:
                logger.error(f"Failed to send simple SMS: {response_data}")
                return {
                    'success': False,
                    'message': f"SMS sending failed: {response_data.get('message', 'Unknown error')}",
                    'data': response_data
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout sending SMS")
            return {
                'success': False,
                'message': 'SMS sending timeout',
                'data': None
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error sending SMS: {str(e)}")
            return {
                'success': False,
                'message': f'SMS sending error: {str(e)}',
                'data': None
            }

        except Exception as e:
            logger.error(f"Unexpected error sending simple SMS: {str(e)}")
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}',
                'data': None
            }

    def send_otp(self, phone_number: str, otp_code: str) -> Dict[str, any]:
        """
        ارسال کد OTP

        این متد به صورت خودکار بین ارسال الگو محور و ساده تصمیم می‌گیرد.
        اگر pattern_code تنظیم شده باشد، از الگو استفاده می‌کند (سریع‌تر و ارزان‌تر)
        در غیر این صورت از ارسال ساده استفاده می‌کند.

        Args:
            phone_number: شماره موبایل گیرنده
            otp_code: کد تایید

        Returns:
            Dict with 'success' and 'message' keys
        """
        if self.pattern_code:
            # Use pattern-based sending (faster and cheaper)
            return self.send_pattern(
                phone_number=phone_number,
                pattern_values={"code": otp_code}
            )
        else:
            # Fallback to simple SMS
            message = f"کد تایید شما در کافی فال:\n{otp_code}\n\nCoffee Fortune verification code: {otp_code}"
            return self.send_simple(
                phone_numbers=[phone_number],
                message=message
            )

    def get_credit(self) -> Dict[str, any]:
        """
        دریافت اعتبار باقیمانده حساب

        Returns:
            Dict with credit information
        """
        try:
            url = f"{self.BASE_URL}/api/v1/sms/credit"

            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )

            response_data = response.json()

            if response.status_code == 200:
                return {
                    'success': True,
                    'credit': response_data.get('credit', 0),
                    'data': response_data
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to get credit',
                    'data': response_data
                }

        except Exception as e:
            logger.error(f"Error getting credit: {str(e)}")
            return {
                'success': False,
                'message': str(e),
                'data': None
            }

    @staticmethod
    def _normalize_phone(phone_number: str) -> str:
        """
        Normalize phone number to international format

        Converts:
            09123456789 -> 989123456789
            9123456789 -> 989123456789
            +989123456789 -> 989123456789
            00989123456789 -> 989123456789
        """
        # Remove all non-digit characters
        phone = ''.join(filter(str.isdigit, phone_number))

        # Handle different formats
        if phone.startswith('0098'):
            phone = phone[2:]
        elif phone.startswith('0'):
            phone = '98' + phone[1:]
        elif not phone.startswith('98'):
            phone = '98' + phone

        return phone

    def is_configured(self) -> bool:
        """Check if the provider is properly configured"""
        return bool(self.api_key and self.originator)


# Factory function to get SMS provider
def get_sms_provider():
    """
    Factory function to get configured SMS provider

    Currently supports:
        - FarazSMSProvider (default)

    You can extend this to support multiple providers
    """
    provider_name = getattr(settings, 'SMS_PROVIDER', 'faraz')

    if provider_name.lower() == 'faraz':
        return FarazSMSProvider()
    else:
        # Add more providers here
        logger.warning(f"Unknown SMS provider: {provider_name}, falling back to FarazSMSProvider")
        return FarazSMSProvider()
