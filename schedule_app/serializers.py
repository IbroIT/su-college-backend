from rest_framework import serializers
from django.utils.translation import get_language
from .models import (
    StudyGroup, Subject, Teacher, Room, 
    TimeSlot, Schedule, ScheduleChange
)


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'name_ru', 'name_en', 'name_ky', 'is_active']
        
    def get_name(self, obj):
        """Возвращает название предмета на текущем языке"""
        language = get_language()
        if language == 'en':
            return obj.name_en
        elif language == 'ky':
            return obj.name_ky
        return obj.name_ru


class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    short_name = serializers.CharField(source='__str__', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 
            'full_name', 'short_name', 'subjects', 'is_active'
        ]


class RoomSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='__str__', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'number', 'full_name', 'is_active'
        ]


class TimeSlotSerializer(serializers.ModelSerializer):
    time_range = serializers.CharField(source='__str__', read_only=True)
    start_time_formatted = serializers.SerializerMethodField()
    end_time_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'number', 'start_time', 'end_time', 'start_time_formatted', 'end_time_formatted', 'time_range', 'is_active']
        
    def get_start_time_formatted(self, obj):
        return obj.start_time.strftime('%H:%M') if obj.start_time else None
        
    def get_end_time_formatted(self, obj):
        return obj.end_time.strftime('%H:%M') if obj.end_time else None


class ScheduleChangeSerializer(serializers.ModelSerializer):
    change_type_display = serializers.CharField(source='get_change_type_display', read_only=True)
    new_teacher = TeacherSerializer(read_only=True)
    new_room = RoomSerializer(read_only=True)
    new_time_slot = TimeSlotSerializer(read_only=True)
    
    class Meta:
        model = ScheduleChange
        fields = [
            'id', 'change_type', 'change_type_display', 'change_date',
            'new_teacher', 'new_room', 'new_time_slot', 'reason',
            'created_by', 'created_at'
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    group = StudyGroupSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    lesson_type_display = serializers.CharField(source='get_lesson_type_display', read_only=True)
    week_type_display = serializers.CharField(source='get_week_type_display', read_only=True)
    
    changes = ScheduleChangeSerializer(source='schedulechange_set', many=True, read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'group', 'subject', 'teacher', 'room', 'time_slot',
            'weekday', 'weekday_display', 'lesson_type', 'lesson_type_display',
            'week_type', 'week_type_display', 'start_date', 'end_date',
            'is_active', 'notes', 'changes'
        ]


class ScheduleListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка расписаний"""
    group_id = serializers.IntegerField(source='group.id', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    subject_name = serializers.SerializerMethodField()
    subject_name_ru = serializers.CharField(source='subject.name_ru', read_only=True)
    subject_name_en = serializers.CharField(source='subject.name_en', read_only=True)
    subject_name_ky = serializers.CharField(source='subject.name_ky', read_only=True)
    teacher_name = serializers.CharField(source='teacher.__str__', read_only=True)
    room_name = serializers.CharField(source='room.__str__', read_only=True)
    time_slot = serializers.IntegerField(source='time_slot.number', read_only=True)
    time_range = serializers.CharField(source='time_slot.__str__', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    lesson_type_display = serializers.CharField(source='get_lesson_type_display', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'group_id', 'group_name', 'subject_name', 'subject_name_ru', 'subject_name_en', 'subject_name_ky',
            'teacher_name', 'room_name', 'time_slot', 'time_range', 'weekday', 'weekday_display', 
            'lesson_type', 'lesson_type_display', 'week_type', 'is_active'
        ]
        
    def get_subject_name(self, obj):
        """Возвращает название предмета на текущем языке"""
        language = get_language()
        if language == 'en':
            return obj.subject.name_en
        elif language == 'ky':
            return obj.subject.name_ky
        return obj.subject.name_ru


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления расписания"""
    
    class Meta:
        model = Schedule
        fields = [
            'group', 'subject', 'teacher', 'room', 'time_slot',
            'weekday', 'lesson_type', 'week_type', 'start_date', 
            'end_date', 'notes', 'is_active'
        ]
        
    def validate(self, data):
        """Дополнительная валидация"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                "Дата начала не может быть позже даты окончания"
            )
        return data