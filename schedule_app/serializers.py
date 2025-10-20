from rest_framework import serializers
from .models import StudyGroup, Teacher, Classroom, Subject, LessonType, TimeSlot, Schedule, ScheduleFeature, ScheduleStat

class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'full_name_ru', 'full_name_kg', 'full_name_en', 
                 'course', 'department', 'is_active', 'order']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'position_ru', 'position_kg', 
                 'position_en', 'department', 'email', 'phone', 'is_active']

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'number', 'building', 'capacity', 'room_type_ru', 
                 'room_type_kg', 'room_type_en', 'equipment', 'is_active']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'code', 'credits', 
                 'hours_total', 'hours_lecture', 'hours_practice', 'hours_lab', 'is_active']

class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'color', 
                 'short_name_ru', 'short_name_kg', 'short_name_en', 'order']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'number', 'start_time', 'end_time', 'order']

class ScheduleSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)
    groups = StudyGroupSerializer(many=True, read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'day_of_week', 'time_slot', 'week_type', 'subject', 
                 'teacher', 'classroom', 'groups', 'lesson_type', 'subgroup',
                 'is_active', 'start_date', 'end_date']

class ScheduleFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleFeature
        fields = ['id', 'icon', 'title_ru', 'title_kg', 'title_en', 
                 'description_ru', 'description_kg', 'description_en', 'color', 'order']

class ScheduleStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleStat
        fields = ['number', 'label_ru', 'label_kg', 'label_en', 'order']