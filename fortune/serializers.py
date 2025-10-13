from rest_framework import serializers
from .models import FortuneFeature, Reading, ReadingHistory


class FortuneFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for FortuneFeature model.
    """
    class Meta:
        model = FortuneFeature
        fields = [
            'id',
            'name',
            'feature_type',
            'input_type',
            'description',
            'credit_cost',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ReadingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new reading.
    """
    feature_type = serializers.CharField(write_only=True)
    language = serializers.ChoiceField(
        choices=[('en', 'English'), ('fa', 'Persian')],
        default='en',
        required=False
    )

    class Meta:
        model = Reading
        fields = [
            'id',
            'feature_type',
            'text_input',
            'image',
            'language',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, data):
        """
        Validate that the correct input is provided based on feature type.
        """
        feature_type = data.get('feature_type')
        text_input = data.get('text_input')
        image = data.get('image')

        try:
            feature = FortuneFeature.objects.get(
                feature_type=feature_type,
                is_active=True
            )
        except FortuneFeature.DoesNotExist:
            raise serializers.ValidationError(
                f"Feature '{feature_type}' is not available."
            )

        # Validate input based on feature requirements
        if feature.input_type == 'text':
            if not text_input:
                raise serializers.ValidationError(
                    "Text input is required for this feature."
                )
        elif feature.input_type == 'image':
            if not image:
                raise serializers.ValidationError(
                    "Image is required for this feature."
                )
        elif feature.input_type == 'text_image':
            if not text_input and not image:
                raise serializers.ValidationError(
                    "Either text or image input is required for this feature."
                )

        data['feature'] = feature
        return data

    def create(self, validated_data):
        """
        Create a new reading.
        """
        feature = validated_data.pop('feature')
        validated_data.pop('feature_type')

        reading = Reading.objects.create(
            feature=feature,
            user=self.context['request'].user,
            **validated_data
        )

        return reading


class ReadingSerializer(serializers.ModelSerializer):
    """
    Serializer for Reading model.
    """
    feature = FortuneFeatureSerializer(read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Reading
        fields = [
            'id',
            'user_phone',
            'feature',
            'text_input',
            'image',
            'language',
            'interpretation',
            'status',
            'error_message',
            'model_used',
            'tokens_used',
            'processing_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user_phone',
            'interpretation',
            'status',
            'error_message',
            'model_used',
            'tokens_used',
            'processing_time',
            'created_at',
            'updated_at',
        ]


class ReadingHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for ReadingHistory model.
    """
    reading = ReadingSerializer(read_only=True)
    feature = FortuneFeatureSerializer(read_only=True)

    class Meta:
        model = ReadingHistory
        fields = [
            'id',
            'feature',
            'reading',
            'rating',
            'feedback',
            'created_at',
        ]
        read_only_fields = ['id', 'feature', 'reading', 'created_at']


class ReadingFeedbackSerializer(serializers.Serializer):
    """
    Serializer for submitting reading feedback.
    """
    rating = serializers.IntegerField(min_value=1, max_value=5)
    feedback = serializers.CharField(required=False, allow_blank=True)
