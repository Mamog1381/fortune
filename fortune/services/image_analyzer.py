import base64
from pathlib import Path
from typing import Optional
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """
    Service for handling image analysis and preparation for vision models.
    """

    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp']
    MAX_SIZE_MB = 10

    @staticmethod
    def validate_image(image: InMemoryUploadedFile) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded image file.
        Returns (is_valid, error_message)
        """
        # Check file extension
        file_extension = image.name.split('.')[-1].lower()
        if file_extension not in ImageAnalyzer.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Allowed: {', '.join(ImageAnalyzer.SUPPORTED_FORMATS)}"

        # Check file size
        size_mb = image.size / (1024 * 1024)
        if size_mb > ImageAnalyzer.MAX_SIZE_MB:
            return False, f"File too large. Maximum size: {ImageAnalyzer.MAX_SIZE_MB}MB"

        return True, None

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """
        Encode image file to base64 string.
        """
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image: {str(e)}")
            raise

    @staticmethod
    def get_image_data_url(image_path: str) -> str:
        """
        Convert image to data URL for API requests.
        """
        try:
            # Get file extension
            extension = Path(image_path).suffix.lower().replace('.', '')
            if extension == 'jpg':
                extension = 'jpeg'

            # Read and encode image
            base64_image = ImageAnalyzer.encode_image_to_base64(image_path)

            # Create data URL
            return f"data:image/{extension};base64,{base64_image}"

        except Exception as e:
            logger.error(f"Error creating data URL: {str(e)}")
            raise

    @staticmethod
    def prepare_image_for_api(image_path: str, use_url: bool = False) -> str:
        """
        Prepare image for API request.
        If use_url is True, returns HTTP URL (requires public URL)
        Otherwise, returns base64 data URL
        """
        if use_url:
            # In production, you might want to use S3 or similar
            # For now, we'll use data URLs
            pass

        return ImageAnalyzer.get_image_data_url(image_path)
