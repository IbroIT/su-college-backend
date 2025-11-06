from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Q
from django import forms
from .models import (
    StudyGroup, Subject, Teacher, Room, 
    TimeSlot, Schedule, ScheduleChange
)


class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Получаем данные
        group = cleaned_data.get('group')
        teacher = cleaned_data.get('teacher')
        room = cleaned_data.get('room')
        weekday = cleaned_data.get('weekday')
        time_slot = cleaned_data.get('time_slot')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if not all([group, teacher, room, weekday, time_slot, start_date, end_date]):
            return cleaned_data
        
        # Проверяем только конфликт для группы (студенты не могут быть в двух местах одновременно)
        existing_schedule = Schedule.objects.filter(
            group=group,
            weekday=weekday,
            time_slot=time_slot,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        # Исключаем текущую запись при редактировании
        if self.instance.pk:
            existing_schedule = existing_schedule.exclude(pk=self.instance.pk)
        
        if existing_schedule.exists():
            raise forms.ValidationError(
                _('Группа {} уже имеет занятие в {} в {} пару с {} по {}').format(
                    group.name,
                    Schedule.WEEKDAY_CHOICES[weekday][1],
                    time_slot.number,
                    start_date,
                    end_date
                )
            )
        
        # НЕ проверяем конфликты для преподавателя и аудитории - разрешаем поточные лекции
        
        return cleaned_data


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'name_ky', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name_ru', 'name_en', 'name_ky']
    ordering = ['name_ru']
    
    fieldsets = (
        (_('Названия на языках'), {
            'fields': ('name_ru', 'name_en', 'name_ky', 'is_active')
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'middle_name']
    filter_horizontal = ['subjects']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        (_('Личная информация'), {
            'fields': ('first_name', 'last_name', 'middle_name')
        }),
        (_('Работа'), {
            'fields': ('subjects', 'is_active')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('ФИО')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'is_active']
    list_filter = ['is_active']
    search_fields = ['number']
    ordering = ['number']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('number', 'is_active')
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['number', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active']
    ordering = ['number']


class ScheduleChangeInline(admin.TabularInline):
    model = ScheduleChange
    extra = 0
    readonly_fields = ['created_at']
    fields = ['change_type', 'change_date', 'new_teacher', 'new_room', 'new_time_slot', 'reason']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = [
        'group', 'subject_display', 'teacher', 'room', 
        'weekday_display', 'time_slot', 'lesson_type_display', 
        'week_type', 'is_active'
    ]
    list_filter = [
        'weekday', 'lesson_type', 'week_type', 'is_active'
    ]
    search_fields = [
        'group__name', 'subject__name_ru', 'subject__name_en', 'subject__name_ky',
        'teacher__first_name', 'teacher__last_name', 'room__number'
    ]
    ordering = ['weekday', 'time_slot__number', 'group__name']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('group', 'subject', 'teacher', 'room')
        }),
        (_('Время и день'), {
            'fields': ('weekday', 'time_slot', 'week_type')
        }),
        (_('Тип и период'), {
            'fields': ('lesson_type', 'start_date', 'end_date')
        }),
        (_('Дополнительно'), {
            'fields': ('notes', 'is_active')
        }),
    )
    
    inlines = [ScheduleChangeInline]
    
    # Фильтры для удобства
    autocomplete_fields = ['group', 'subject', 'teacher', 'room']
    
    def subject_display(self, obj):
        return obj.subject.name_ru
    subject_display.short_description = _('Предмет')
    
    def weekday_display(self, obj):
        return obj.get_weekday_display()
    weekday_display.short_description = _('День недели')
    
    def lesson_type_display(self, obj):
        color_map = {
            'lecture': '#3498db',
            'practice': '#9b59b6',
            'lab': '#2ecc71',
            'seminar': '#f39c12',
            'exam': '#e74c3c',
            'module': '#e67e22',
            'consultation': '#1abc9c',
            'project': '#e91e63',
            'elective': '#ff9800',
            'club': '#9c27b0',
            'sports': '#f44336',
        }
        color = color_map.get(obj.lesson_type, '#95a5a6')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_lesson_type_display()
        )
    lesson_type_display.short_description = _('Тип занятия')
    
    # Дополнительные действия
    actions = ['duplicate_schedule', 'activate_schedule', 'deactivate_schedule']
    
    def duplicate_schedule(self, request, queryset):
        for schedule in queryset:
            schedule.pk = None
            schedule.save()
        self.message_user(request, _('Выбранные расписания были продублированы'))
    duplicate_schedule.short_description = _('Дублировать выбранные расписания')
    
    def activate_schedule(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _('Выбранные расписания активированы'))
    activate_schedule.short_description = _('Активировать выбранные расписания')
    
    def deactivate_schedule(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _('Выбранные расписания деактивированы'))
    deactivate_schedule.short_description = _('Деактивировать выбранные расписания')


@admin.register(ScheduleChange)
class ScheduleChangeAdmin(admin.ModelAdmin):
    list_display = [
        'original_schedule', 'change_type', 'change_date', 
        'created_by', 'created_at'
    ]
    list_filter = ['change_type', 'change_date', 'created_at']
    search_fields = [
        'original_schedule__group__name', 
        'original_schedule__subject__name_ru',
        'reason', 'created_by'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('original_schedule', 'change_type', 'change_date')
        }),
        (_('Новые данные'), {
            'fields': ('new_teacher', 'new_room', 'new_time_slot')
        }),
        (_('Дополнительно'), {
            'fields': ('reason', 'created_by', 'created_at')
        }),
    )


# Настройка админки
admin.site.site_header = _('Администрирование расписания колледжа')
admin.site.site_title = _('Расписание колледжа')
admin.site.index_title = _('Добро пожаловать в панель управления расписанием')