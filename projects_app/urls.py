from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.StudentProjectViewSet)
router.register(r'stats', views.ProjectStatViewSet)
router.register(r'data', views.ProjectsDataViewSet, basename='projects-data')

urlpatterns = [
    path('', include(router.urls)),
]