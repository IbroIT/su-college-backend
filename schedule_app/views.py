from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from django.utils import timezone
from datetime import datetime, timedelta
from .models import StudyGroup, Schedule, ScheduleFeature, ScheduleStat, TimeSlot, LessonType
from .serializers import StudyGroupSerializer, ScheduleSerializer, ScheduleFeatureSerializer, ScheduleStatSerializer, TimeSlotSerializer, LessonTypeSerializer

class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.filter(is_active=True)
    serializer_class = StudyGroupSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить группы с переводами"""
        language = get_language()
        groups = StudyGroup.objects.filter(is_active=True).order_by('course', 'name')
        
        data = []
        for group in groups:
            data.append({
                'id': group.id,
                'name': group.name,
                'full_name': getattr(group, f'full_name_{language}', group.full_name_ru),
                'course': group.course,
                'department': group.department
            })
        
        return Response(data)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.filter(is_active=True)
    serializer_class = ScheduleSerializer
    
    @action(detail=False, methods=['get'])
    def by_group_and_day(self, request):
        """Получить расписание по группе и дню"""
        language = get_language()
        group_id = request.GET.get('group', 'all')
        day_of_week = int(request.GET.get('day', 0))
        
        # Определяем текущую неделю (числитель/знаменатель)
        today = timezone.now().date()
        start_of_semester = today - timedelta(days=today.weekday())  # Начало текущей недели
        week_number = start_of_semester.isocalendar()[1]
        week_type = 'numerator' if week_number % 2 == 1 else 'denominator'
        
        # Фильтруем расписание
        schedules = Schedule.objects.filter(
            is_active=True,
            day_of_week=day_of_week,
            start_date__lte=today,
            end_date__gte=today
        ).select_related('subject', 'teacher', 'classroom', 'lesson_type', 'time_slot').prefetch_related('groups')
        
        # Фильтр по группе
        if group_id != 'all':
            schedules = schedules.filter(groups__id=group_id)
        
        # Фильтр по типу недели
        schedules = schedules.filter(week_type__in=[week_type, 'both'])
        
        schedules = schedules.order_by('time_slot__number')
        
        data = {}
        for schedule in schedules:
            time_slot_id = schedule.time_slot.number
            
            if time_slot_id not in data:
                data[time_slot_id] = []
            
            schedule_data = {
                'subject': getattr(schedule.subject, f'name_{language}', schedule.subject.name_ru),
                'teacher': getattr(schedule.teacher, f'name_{language}', schedule.teacher.name_ru),
                'classroom': {
                    'number': schedule.classroom.number,
                    'building': schedule.classroom.building,
                    'type': getattr(schedule.classroom, f'room_type_{language}', schedule.classroom.room_type_ru)
                },
                'lesson_type': {
                    'name': getattr(schedule.lesson_type, f'name_{language}', schedule.lesson_type.name_ru),
                    'short_name': getattr(schedule.lesson_type, f'short_name_{language}', schedule.lesson_type.short_name_ru),
                    'color': schedule.lesson_type.color
                },
                'groups': [group.name for group in schedule.groups.all()],
                'subgroup': schedule.subgroup,
                'time_slot': {
                    'number': schedule.time_slot.number,
                    'start_time': schedule.time_slot.start_time.strftime('%H:%M'),
                    'end_time': schedule.time_slot.end_time.strftime('%H:%M')
                }
            }
            data[time_slot_id].append(schedule_data)
        
        return Response(data)

class ScheduleFeatureViewSet(viewsets.ModelViewSet):
    queryset = ScheduleFeature.objects.all()
    serializer_class = ScheduleFeatureSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить особенности с переводами"""
        language = get_language()
        features = ScheduleFeature.objects.all().order_by('order')
        
        data = []
        for feature in features:
            data.append({
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color
            })
        
        return Response(data)

class ScheduleStatViewSet(viewsets.ModelViewSet):
    queryset = ScheduleStat.objects.all()
    serializer_class = ScheduleStatSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить статистику с переводами"""
        language = get_language()
        stats = ScheduleStat.objects.all().order_by('order')
        
        data = []
        for stat in stats:
            data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response(data)

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all().order_by('number')
    serializer_class = TimeSlotSerializer
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """Получить все временные слоты"""
        time_slots = TimeSlot.objects.all().order_by('number')
        data = []
        for slot in time_slots:
            data.append({
                'id': slot.number,
                'time': f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}",
                'number': slot.number
            })
        return Response(data)

class LessonTypeViewSet(viewsets.ModelViewSet):
    queryset = LessonType.objects.all().order_by('order')
    serializer_class = LessonTypeSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить типы занятий с переводами"""
        language = get_language()
        lesson_types = LessonType.objects.all().order_by('order')
        
        data = []
        for lesson_type in lesson_types:
            data.append({
                'name': getattr(lesson_type, f'name_{language}', lesson_type.name_ru),
                'short_name': getattr(lesson_type, f'short_name_{language}', lesson_type.short_name_ru),
                'color': lesson_type.color
            })
        
        return Response(data)

class ScheduleDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        """Получить все данные расписания"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        # Группы
        groups = StudyGroup.objects.filter(is_active=True).order_by('course', 'name')
        groups_data = []
        for group in groups:
            groups_data.append({
                'id': group.name.lower().replace(' ', '-'),
                'name': group.name,
                'full_name': getattr(group, f'full_name_{language}', group.full_name_ru)
            })
        
        # Особенности
        features = ScheduleFeature.objects.all().order_by('order')
        features_data = []
        for feature in features:
            features_data.append({
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color
            })
        
        # Статистика
        stats = ScheduleStat.objects.all().order_by('order')
        stats_data = []
        for stat in stats:
            stats_data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        # Временные слоты
        time_slots = TimeSlot.objects.all().order_by('number')
        time_slots_data = []
        for slot in time_slots:
            time_slots_data.append({
                'id': slot.number,
                'time': f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}"
            })
        
        # Типы занятий
        lesson_types = LessonType.objects.all().order_by('order')
        lesson_types_data = {}
        for lesson_type in lesson_types:
            lesson_types_data[lesson_type.name_ru] = {
                'name': getattr(lesson_type, f'name_{language}', lesson_type.name_ru),
                'color': lesson_type.color
            }
        
        return Response({
            'groups': groups_data,
            'features': features_data,
            'stats': stats_data,
            'timeSlots': time_slots_data,
            'lessonTypes': lesson_types_data
        })