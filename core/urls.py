from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.viewsets import (
    UserViewSet, TransportCardViewSet,
    RideViewSet, TopUpViewSet, BlockViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'cards', TransportCardViewSet, basename='card')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'topups', TopUpViewSet, basename='topup')
router.register(r'blocks', BlockViewSet, basename='block')

urlpatterns = [
    path('', include(router.urls)),
]
