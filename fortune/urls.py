from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FortuneFeatureViewSet, ReadingViewSet, ReadingHistoryViewSet

router = DefaultRouter()
router.register(r'features', FortuneFeatureViewSet, basename='fortune-feature')
router.register(r'readings', ReadingViewSet, basename='reading')
router.register(r'history', ReadingHistoryViewSet, basename='reading-history')

urlpatterns = [
    path('', include(router.urls)),
]
