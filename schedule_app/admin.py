from django.contrib import admin
from .models import StudyGroup, Teacher, Classroom, Subject, LessonType, TimeSlot, Schedule, ScheduleFeature, ScheduleStat

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name_ru', 'course', 'department', 'is_active', 'order']
    list_filter = ['course', 'department', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'full_name_ru', 'full_name_kg', 'full_name_en']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'position_ru', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['name_ru', 'name_kg', 'name_en']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['number', 'building', 'room_type_ru', 'capacity', 'is_active']
    list_filter = ['building', 'is_active']
    search_fields = ['number', 'building']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'code', 'credits', 'hours_total', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name_ru', 'name_kg', 'name_en', 'code']

@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'short_name_ru', 'color', 'order']
    list_editable = ['order']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['number', 'start_time', 'end_time', 'order']
    list_editable = ['order']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'time_slot', 'subject', 'teacher', 'classroom', 'week_type', 'is_active']
    list_filter = ['day_of_week', 'week_type', 'is_active', 'lesson_type']
    list_editable = ['is_active']
    filter_horizontal = ['groups']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('day_of_week', 'time_slot', 'week_type')
        }),
        ('Занятие', {
            'fields': ('subject', 'teacher', 'classroom', 'lesson_type', 'groups', 'subgroup')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date')
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(ScheduleFeature)
class ScheduleFeatureAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'icon', 'color', 'order']
    list_editable = ['order']

@admin.register(ScheduleStat)
class ScheduleStatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label_ru', 'order']
    list_editable = ['order']