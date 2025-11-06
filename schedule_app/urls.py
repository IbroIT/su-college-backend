from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudyGroupViewSet, SubjectViewSet, TeacherViewSet,
    RoomViewSet, TimeSlotViewSet, ScheduleViewSet,
    ScheduleChangeViewSet
)

router = DefaultRouter()
router.register(r'groups', StudyGroupViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'schedule-changes', ScheduleChangeViewSet)

app_name = 'schedule_app'

urlpatterns = [
    path('api/', include(router.urls)),
]