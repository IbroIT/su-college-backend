from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import CouncilFeature, CouncilMember, CouncilEvent, CouncilStat

@admin.register(CouncilFeature)
class CouncilFeatureAdmin(ModelAdmin):
    list_display = ['title_ru', 'icon', 'color', 'order']
    list_editable = ['order']
    list_filter = ['order']

@admin.register(CouncilMember)
class CouncilMemberAdmin(ModelAdmin):
    list_display = ['name_ru', 'position_ru', 'position_type', 'is_active', 'order']
    list_filter = ['position_type', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name_ru', 'name_kg', 'name_en']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name_ru', 'name_kg', 'name_en', 'position_ru', 'position_kg', 'position_en')
        }),
        ('Биография', {
            'fields': ('bio_ru', 'bio_kg', 'bio_en')
        }),
        ('Контакты и фото', {
            'fields': ('image', 'instagram', 'email', 'linkedin')
        }),
        ('Настройки', {
            'fields': ('position_type', 'is_active', 'order')
        }),
    )

@admin.register(CouncilEvent)
class CouncilEventAdmin(ModelAdmin):
    list_display = ['title_ru', 'date', 'participants', 'is_active']
    list_filter = ['is_active', 'date']
    list_editable = ['is_active']
    date_hierarchy = 'date'

@admin.register(CouncilStat)
class CouncilStatAdmin(ModelAdmin):
    list_display = ['number', 'label_ru', 'order']
    list_editable = ['order']