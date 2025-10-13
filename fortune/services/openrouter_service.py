import requests
import time
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class OpenRouterService:
    """
    Service for interacting with OpenRouter.ai API.
    Handles text and vision model requests.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'OPENROUTER_API_KEY', None)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        messages: list,
        model: str = "google/gemini-2.0-flash-exp:free",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Make a request to OpenRouter.ai API.
        """
        if not self.api_key:
            logger.warning("OpenRouter API key not configured")
            return {
                'success': False,
                'error': 'API key not configured',
                'mock_response': True,
                'content': self._generate_mock_response(messages)
            }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            start_time = time.time()
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            processing_time = time.time() - start_time

            response.raise_for_status()
            data = response.json()

            return {
                'success': True,
                'content': data['choices'][0]['message']['content'],
                'model': data.get('model', model),
                'tokens_used': data.get('usage', {}).get('total_tokens', 0),
                'processing_time': processing_time,
                'mock_response': False,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'mock_response': True,
                'content': self._generate_mock_response(messages)
            }

    def generate_text_interpretation(
        self,
        prompt: str,
        model: str = "google/gemini-2.0-flash-exp:free",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate text-based interpretation (for dream interpretation, horoscopes, etc.)
        """
        messages = [
            {
                "role": "system",
                "content": "You are a mystical fortune teller and interpreter. Provide engaging, creative, and entertaining interpretations while being respectful of cultural traditions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self._make_request(messages, model, max_tokens, temperature)

    def generate_image_interpretation(
        self,
        prompt: str,
        image_url: str,
        model: str = "google/gemini-2.0-flash-exp:free",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate interpretation from an image (for coffee fortune, feng shui, palm reading, etc.)
        """
        messages = [
            {
                "role": "system",
                "content": "You are a mystical fortune teller and interpreter. Analyze images and provide engaging, creative, and entertaining interpretations while being respectful of cultural traditions."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]

        return self._make_request(messages, model, max_tokens, temperature)

    def _generate_mock_response(self, messages: list) -> str:
        """
        Generate a mock response when API key is not configured.
        This is useful for development and testing.
        """
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    user_message = content
                elif isinstance(content, list):
                    for item in content:
                        if item.get("type") == "text":
                            user_message = item.get("text", "")
                            break

        return f"""
🔮 MOCK RESPONSE - API Key Not Configured 🔮

This is a demonstration response. To get real interpretations, please configure your OpenRouter.ai API key.

Your request: {user_message[:100]}...

[In production, this would be replaced with an actual AI-generated interpretation based on the mystical practice you've chosen.]

To enable real interpretations:
1. Get an API key from https://openrouter.ai
2. Set OPENROUTER_API_KEY in your environment variables
3. Restart the application

Thank you for using our mystical services!
        """.strip()

    def check_api_status(self) -> Dict[str, Any]:
        """
        Check if the API key is configured and working.
        """
        if not self.api_key:
            return {
                'configured': False,
                'working': False,
                'message': 'API key not configured'
            }

        try:
            response = self.generate_text_interpretation(
                "Test message",
                max_tokens=10
            )
            return {
                'configured': True,
                'working': response['success'],
                'message': 'API is working' if response['success'] else response.get('error', 'Unknown error')
            }
        except Exception as e:
            return {
                'configured': True,
                'working': False,
                'message': str(e)
            }
