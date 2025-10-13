from celery import shared_task
from django.conf import settings
from django.utils import timezone
import time
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_reading(self, reading_id: str):
    """
    Process a fortune reading asynchronously.
    This task handles both text and image-based readings.
    """
    from .models import Reading, ReadingHistory
    from .services import OpenRouterService, ImageAnalyzer

    try:
        # Get the reading
        reading = Reading.objects.get(id=reading_id)
        reading.status = 'processing'
        reading.save()

        logger.info(f"Processing reading {reading_id} for feature {reading.feature.feature_type}")

        # Initialize OpenRouter service
        openrouter = OpenRouterService()

        # Prepare the prompt
        prompt = reading.feature.prompt_template

        # Add language instruction to prompt
        language_instructions = {
            'fa': '\n\nIMPORTANT: Please provide your response in Persian (Farsi) language. Use Persian script and maintain cultural sensitivity for Iranian/Persian traditions.',
            'en': ''
        }
        language_instruction = language_instructions.get(reading.language, '')
        prompt = prompt + language_instruction

        # Replace placeholders
        if reading.text_input:
            prompt = prompt.replace('{user_input}', reading.text_input)

        # Handle image-based readings
        if reading.image and reading.feature.input_type in ['image', 'text_image']:
            try:
                # Get the full image path
                image_path = reading.image.path

                # Prepare image for API
                image_data = ImageAnalyzer.prepare_image_for_api(image_path)

                # Generate interpretation with image
                start_time = time.time()
                result = openrouter.generate_image_interpretation(
                    prompt=prompt,
                    image_url=image_data,
                    model=reading.feature.model_name,
                    max_tokens=reading.feature.max_tokens,
                    temperature=reading.feature.temperature,
                )

            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                raise

        else:
            # Text-only reading
            start_time = time.time()
            result = openrouter.generate_text_interpretation(
                prompt=prompt,
                model=reading.feature.model_name,
                max_tokens=reading.feature.max_tokens,
                temperature=reading.feature.temperature,
            )

        # Update reading with results
        if result['success'] or result.get('mock_response'):
            reading.interpretation = result['content']
            reading.status = 'completed'
            reading.model_used = result.get('model', reading.feature.model_name)
            reading.tokens_used = result.get('tokens_used', 0)
            reading.processing_time = result.get('processing_time', time.time() - start_time)

            # Create history entry
            ReadingHistory.objects.create(
                user=reading.user,
                feature=reading.feature,
                reading=reading
            )

            logger.info(f"Reading {reading_id} completed successfully")

        else:
            reading.status = 'failed'
            reading.error_message = result.get('error', 'Unknown error occurred')
            logger.error(f"Reading {reading_id} failed: {reading.error_message}")

        reading.save()

        return {
            'reading_id': str(reading.id),
            'status': reading.status,
            'success': reading.status == 'completed'
        }

    except Reading.DoesNotExist:
        logger.error(f"Reading {reading_id} not found")
        return {'success': False, 'error': 'Reading not found'}

    except Exception as e:
        logger.error(f"Error processing reading {reading_id}: {str(e)}")

        try:
            reading = Reading.objects.get(id=reading_id)
            reading.status = 'failed'
            reading.error_message = str(e)
            reading.save()
        except:
            pass

        # Retry the task
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))

        return {'success': False, 'error': str(e)}


@shared_task
def cleanup_old_readings():
    """
    Periodic task to clean up old failed readings.
    Run this daily via Celery Beat.
    """
    from .models import Reading
    from django.utils import timezone
    from datetime import timedelta

    # Delete failed readings older than 7 days
    cutoff_date = timezone.now() - timedelta(days=7)
    deleted_count, _ = Reading.objects.filter(
        status='failed',
        created_at__lt=cutoff_date
    ).delete()

    logger.info(f"Cleaned up {deleted_count} old failed readings")

    return {'deleted_count': deleted_count}


@shared_task
def generate_daily_horoscope():
    """
    Example task for generating daily horoscopes.
    This can be scheduled via Celery Beat.
    """
    logger.info("Generating daily horoscopes...")
    # Implementation will depend on your requirements
    pass
