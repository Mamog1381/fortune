from django.db import models
from django.conf import settings
import uuid


class FortuneFeature(models.Model):
    """
    Represents different fortune-telling features available in the app.
    Each feature has its own prompt template and configuration.
    """
    FEATURE_TYPES = [
        ('coffee_fortune', 'Coffee Fortune Reading'),
        ('feng_shui', 'Feng Shui Analysis'),
        ('dream_interpretation', 'Dream Interpretation'),
        ('birthdate_horoscope', 'Birthdate Horoscope'),
        ('tarot', 'Tarot Reading'),
        ('numerology', 'Numerology'),
        ('palm_reading', 'Palm Reading'),
    ]

    INPUT_TYPES = [
        ('text', 'Text Input'),
        ('image', 'Image Input'),
        ('text_image', 'Text and Image Input'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    feature_type = models.CharField(max_length=50, choices=FEATURE_TYPES, unique=True)
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES)
    description = models.TextField()
    prompt_template = models.TextField(
        help_text="Template for the prompt. Use {user_input} and {image_description} as placeholders."
    )
    is_active = models.BooleanField(default=True)

    # OpenRouter.ai model configuration
    model_name = models.CharField(
        max_length=100,
        default='openai/gpt-4o-mini',
        help_text='OpenRouter.ai model identifier'
    )
    max_tokens = models.IntegerField(default=1000)
    temperature = models.FloatField(default=0.7)

    # Pricing and limits
    credit_cost = models.IntegerField(
        default=1,
        help_text='Credits required per reading'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Fortune Feature'
        verbose_name_plural = 'Fortune Features'

    def __str__(self):
        return self.name


class Reading(models.Model):
    """
    Stores individual fortune readings/interpretations.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='readings'
    )
    feature = models.ForeignKey(
        FortuneFeature,
        on_delete=models.CASCADE,
        related_name='readings'
    )

    # Input data
    text_input = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='readings/%Y/%m/%d/',
        blank=True,
        null=True
    )

    # Output data
    interpretation = models.TextField(blank=True, null=True)

    # Processing metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(blank=True, null=True)

    # OpenRouter.ai metadata
    model_used = models.CharField(max_length=100, blank=True, null=True)
    tokens_used = models.IntegerField(default=0)
    processing_time = models.FloatField(
        default=0,
        help_text='Processing time in seconds'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reading'
        verbose_name_plural = 'Readings'

    def __str__(self):
        return f"{self.user.phone_number} - {self.feature.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ReadingHistory(models.Model):
    """
    Tracks user's reading history for analytics and recommendations.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reading_history'
    )
    feature = models.ForeignKey(
        FortuneFeature,
        on_delete=models.CASCADE
    )
    reading = models.OneToOneField(
        Reading,
        on_delete=models.CASCADE,
        related_name='history'
    )

    # User feedback
    rating = models.IntegerField(
        blank=True,
        null=True,
        help_text='User rating from 1-5'
    )
    feedback = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reading History'
        verbose_name_plural = 'Reading Histories'

    def __str__(self):
        return f"{self.user.phone_number} - {self.feature.name}"
