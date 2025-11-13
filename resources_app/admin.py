from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ResourceCategory, EducationalResource, LibraryFeature, LibraryStat, WorkingHours

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(ModelAdmin):
    list_display = ['name_ru', 'icon', 'color', 'order']
    list_editable = ['order']
    list_filter = ['order']

@admin.register(EducationalResource)
class EducationalResourceAdmin(ModelAdmin):
    list_display = ['title_ru', 'category', 'resource_type', 'access_type', 'count', 'pinned', 'is_available', 'order']
    list_filter = ['category', 'resource_type', 'access_type', 'pinned', 'is_available']
    list_editable = ['pinned', 'is_available', 'order']
    search_fields = ['title_ru', 'title_kg', 'title_en', 'description_ru']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title_ru', 'title_kg', 'title_en',
                'description_ru', 'description_kg', 'description_en',
                'category'
            )
        }),
        ('Тип и доступ', {
            'fields': (
                'resource_type', 'access_type',
            )
        }),
        ('Количественные данные', {
            'fields': (
                'count', 'available_count',
            )
        }),
        ('Ссылки и файлы', {
            'fields': (
                'access_url', 'download_url', 'document_file',
            )
        }),
        ('Настройки', {
            'fields': (
                'is_featured', 'is_available', 'order',
            )
        }),
    )

@admin.register(LibraryFeature)
class LibraryFeatureAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'icon', 'color', 'order']
    list_editable = ['order']

@admin.register(LibraryStat)
class LibraryStatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label_ru', 'order']
    list_editable = ['order']

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['day_ru', 'time_ru', 'order']
    list_editable = ['order']