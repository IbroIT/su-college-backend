from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from .models import (
    StudyGroup, Subject, Teacher, Room, 
    TimeSlot, Schedule, ScheduleChange
)
from .serializers import (
    StudyGroupSerializer, SubjectSerializer, TeacherSerializer,
    RoomSerializer, TimeSlotSerializer, ScheduleSerializer,
    ScheduleListSerializer, ScheduleCreateUpdateSerializer,
    ScheduleChangeSerializer
)


class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.filter(is_active=True)
    serializer_class = StudyGroupSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(is_active=True)
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_ru', 'name_en', 'name_ky']
    ordering_fields = ['name_ru']
    ordering = ['name_ru']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'middle_name']
    ordering_fields = ['last_name', 'first_name']
    ordering = ['last_name', 'first_name']


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number']
    ordering_fields = ['number']
    ordering = ['number']


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.filter(is_active=True)
    serializer_class = TimeSlotSerializer
    ordering = ['number']


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'group__name', 'subject__name_ru', 'subject__name_en', 'subject__name_ky',
        'teacher__first_name', 'teacher__last_name', 'room__number'
    ]
    ordering_fields = ['weekday', 'time_slot__number']
    ordering = ['weekday', 'time_slot__number']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ScheduleCreateUpdateSerializer
        return ScheduleSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по дате
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_date__lte=start_date, end_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_date__lte=end_date, end_date__gte=end_date)
            
        # Фильтр по текущей неделе
        current_week = self.request.query_params.get('current_week')
        if current_week == 'true':
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            queryset = queryset.filter(
                start_date__lte=end_of_week,
                end_date__gte=start_of_week
            )
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def weekly_schedule(self, request):
        """Получить расписание на неделю"""
        group_id = request.query_params.get('group_id')
        teacher_id = request.query_params.get('teacher_id')
        room_id = request.query_params.get('room_id')
        week_start = request.query_params.get('week_start')
        
        if not week_start:
            # Если дата не указана, берем текущую неделю
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
        else:
            week_start = datetime.strptime(week_start, '%Y-%m-%d').date()
            
        week_end = week_start + timedelta(days=6)
        
        queryset = self.get_queryset().filter(
            start_date__lte=week_end,
            end_date__gte=week_start
        )
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
            
        # Группируем по дням недели
        schedule_by_day = {}
        for day in range(1, 8):  # 1-7 (понедельник-воскресенье)
            day_schedule = queryset.filter(weekday=day).order_by('time_slot__number')
            schedule_by_day[day] = ScheduleListSerializer(day_schedule, many=True).data
            
        return Response({
            'week_start': week_start,
            'week_end': week_end,
            'schedule': schedule_by_day
        })
    
    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Получить расписание для конкретной группы"""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = self.get_queryset().filter(group_id=group_id)
        serializer = ScheduleListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_teacher(self, request):
        """Получить расписание для конкретного преподавателя"""
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response(
                {'error': 'teacher_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = self.get_queryset().filter(teacher_id=teacher_id)
        serializer = ScheduleListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        """Проверка конфликтов в расписании"""
        queryset = self.get_queryset()
        conflicts = []
        
        for schedule in queryset:
            # Проверяем конфликты преподавателя
            teacher_conflicts = queryset.filter(
                teacher=schedule.teacher,
                weekday=schedule.weekday,
                time_slot=schedule.time_slot,
                start_date__lte=schedule.end_date,
                end_date__gte=schedule.start_date
            ).exclude(id=schedule.id)
            
            if teacher_conflicts.exists():
                conflicts.append({
                    'type': 'teacher_conflict',
                    'schedule': ScheduleListSerializer(schedule).data,
                    'conflicts_with': ScheduleListSerializer(teacher_conflicts, many=True).data
                })
            
            # Проверяем конфликты аудитории
            room_conflicts = queryset.filter(
                room=schedule.room,
                weekday=schedule.weekday,
                time_slot=schedule.time_slot,
                start_date__lte=schedule.end_date,
                end_date__gte=schedule.start_date
            ).exclude(id=schedule.id)
            
            if room_conflicts.exists():
                conflicts.append({
                    'type': 'room_conflict',
                    'schedule': ScheduleListSerializer(schedule).data,
                    'conflicts_with': ScheduleListSerializer(room_conflicts, many=True).data
                })
                
        return Response({'conflicts': conflicts})


class ScheduleChangeViewSet(viewsets.ModelViewSet):
    queryset = ScheduleChange.objects.all()
    serializer_class = ScheduleChangeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reason', 'created_by']
    ordering = ['-created_at']