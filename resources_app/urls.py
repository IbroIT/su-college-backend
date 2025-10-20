from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'resources', views.EducationalResourceViewSet)
router.register(r'features', views.LibraryFeatureViewSet)
router.register(r'stats', views.LibraryStatViewSet)
router.register(r'hours', views.WorkingHoursViewSet)
router.register(r'data', views.ResourcesDataViewSet, basename='resources-data')

urlpatterns = [
    path('', include(router.urls)),
]