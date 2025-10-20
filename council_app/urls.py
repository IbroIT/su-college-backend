from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'features', views.CouncilFeatureViewSet)
router.register(r'members', views.CouncilMemberViewSet)
router.register(r'events', views.CouncilEventViewSet)
router.register(r'stats', views.CouncilStatViewSet)
router.register(r'data', views.CouncilDataViewSet, basename='council-data')

urlpatterns = [
    path('', include(router.urls)),
]