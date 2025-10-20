from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Teacher, Achievement

class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 3
    fields = ['text_ru', 'text_kg', 'text_en', 'order']
    verbose_name = _("Достижение")
    verbose_name_plural = _("Достижения")

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'name_ru', 
        'rating', 
        'is_active', 
        'order',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_ru', 'name_kg', 'name_en']
    list_editable = ['is_active', 'order', 'rating']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_("Основная информация"), {
            'fields': (
                'is_active',
                'order',
            )
        }),
        (_("Имена преподавателя"), {
            'fields': (
                ('name_ru', 'name_kg', 'name_en'),
            )
        }),
        (_("Предметы"), {
            'fields': (
                ('subject_ru', 'subject_kg', 'subject_en'),
            )
        }),
        (_("Опыт работы"), {
            'fields': (
                ('experience_ru', 'experience_kg', 'experience_en'),
            )
        }),
        (_("Описания"), {
            'fields': (
                'description_ru',
                'description_kg', 
                'description_en',
            )
        }),
        (_("Дополнительная информация"), {
            'fields': (
                'rating',
                'color',
                'image',
            )
        }),
        (_("Метаданные"), {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [AchievementInline]
    
    # Группировка полей для удобства
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'text_ru_preview', 'order']
    list_filter = ['teacher']
    search_fields = ['text_ru', 'text_kg', 'text_en', 'teacher__name_ru']
    list_editable = ['order']
    
    def text_ru_preview(self, obj):
        return obj.text_ru[:50] + "..." if len(obj.text_ru) > 50 else obj.text_ru
    text_ru_preview.short_description = _("Достижение (превью)")