from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import FortuneFeature, Reading, ReadingHistory
from .serializers import (
    FortuneFeatureSerializer,
    ReadingCreateSerializer,
    ReadingSerializer,
    ReadingHistorySerializer,
    ReadingFeedbackSerializer,
)
from .tasks import process_reading
from .services import ImageAnalyzer


class FortuneFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing available fortune features.
    """
    queryset = FortuneFeature.objects.filter(is_active=True)
    serializer_class = FortuneFeatureSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Get feature by type.
        Example: /api/fortune/features/by_type/?type=coffee_fortune
        """
        feature_type = request.query_params.get('type')
        if not feature_type:
            return Response(
                {'error': 'Feature type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            feature = FortuneFeature.objects.get(
                feature_type=feature_type,
                is_active=True
            )
            serializer = self.get_serializer(feature)
            return Response(serializer.data)
        except FortuneFeature.DoesNotExist:
            return Response(
                {'error': 'Feature not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ReadingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing fortune readings.
    """
    serializer_class = ReadingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'feature__feature_type']

    def get_queryset(self):
        """
        Return readings for the current user only.
        """
        return Reading.objects.filter(user=self.request.user).select_related('feature')

    def get_serializer_class(self):
        """
        Use different serializers for create and other actions.
        """
        if self.action == 'create':
            return ReadingCreateSerializer
        return ReadingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new reading and process it asynchronously.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validate image if provided
        if 'image' in request.FILES:
            image = request.FILES['image']
            is_valid, error_message = ImageAnalyzer.validate_image(image)
            if not is_valid:
                return Response(
                    {'error': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the reading
        reading = serializer.save()

        # Process asynchronously
        process_reading.delay(str(reading.id))

        # Return the reading
        response_serializer = ReadingSerializer(reading)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def status_check(self, request, pk=None):
        """
        Check the status of a reading.
        """
        reading = self.get_object()
        serializer = self.get_serializer(reading)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """
        Submit feedback for a reading.
        """
        reading = self.get_object()

        # Check if reading is completed
        if reading.status != 'completed':
            return Response(
                {'error': 'Can only provide feedback for completed readings'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate feedback
        feedback_serializer = ReadingFeedbackSerializer(data=request.data)
        feedback_serializer.is_valid(raise_exception=True)

        # Get or create history
        history, created = ReadingHistory.objects.get_or_create(
            reading=reading,
            defaults={
                'user': reading.user,
                'feature': reading.feature,
            }
        )

        # Update feedback
        history.rating = feedback_serializer.validated_data['rating']
        history.feedback = feedback_serializer.validated_data.get('feedback', '')
        history.save()

        return Response({
            'message': 'Feedback submitted successfully',
            'rating': history.rating
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent readings for the current user.
        """
        limit = int(request.query_params.get('limit', 10))
        readings = self.get_queryset()[:limit]
        serializer = self.get_serializer(readings, many=True)
        return Response(serializer.data)


class ReadingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing reading history.
    """
    serializer_class = ReadingHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['feature__feature_type', 'rating']

    def get_queryset(self):
        """
        Return history for the current user only.
        """
        return ReadingHistory.objects.filter(
            user=self.request.user
        ).select_related('feature', 'reading')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get statistics about user's readings.
        """
        history = self.get_queryset()

        # Calculate statistics
        total_readings = history.count()
        features_used = history.values('feature__name').distinct().count()
        avg_rating = history.filter(rating__isnull=False).aggregate(
            avg=models.Avg('rating')
        )['avg']

        # Most used feature
        most_used = history.values('feature__name').annotate(
            count=models.Count('id')
        ).order_by('-count').first()

        return Response({
            'total_readings': total_readings,
            'features_used': features_used,
            'average_rating': round(avg_rating, 2) if avg_rating else None,
            'most_used_feature': most_used['feature__name'] if most_used else None,
            'most_used_count': most_used['count'] if most_used else 0,
        })
