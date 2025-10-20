from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'study-groups', views.StudyGroupViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'features', views.ScheduleFeatureViewSet)
router.register(r'stats', views.ScheduleStatViewSet)
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'lesson-types', views.LessonTypeViewSet)
router.register(r'data', views.ScheduleDataViewSet, basename='schedule-data')

urlpatterns = [
    path('', include(router.urls)),
]