from django.contrib import admin
from .models import StudentProject, ProjectFeature, ProjectTechnology, ProjectStat

class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 4
    fields = ['text_ru', 'text_kg', 'text_en', 'order']

class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 6
    fields = ['name', 'icon', 'color', 'order']

@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ['student_name_ru', 'title_ru', 'is_featured', 'is_published', 'order', 'views']
    list_filter = ['is_featured', 'is_published', 'created_at']
    list_editable = ['is_featured', 'is_published', 'order']
    search_fields = ['student_name_ru', 'student_name_kg', 'student_name_en', 'title_ru']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'student_name_ru', 'student_name_kg', 'student_name_en',
                'title_ru', 'title_kg', 'title_en',
            )
        }),
        ('Описание', {
            'fields': (
                'description_ru', 'description_kg', 'description_en',
            )
        }),
        ('Медиа', {
            'fields': (
                'student_image', 'project_image',
            )
        }),
        ('Ссылки', {
            'fields': (
                'github_url', 'website_url', 'demo_url',
            )
        }),
        ('Настройки', {
            'fields': (
                'is_featured', 'is_published', 'order',
            )
        }),
        ('Статистика', {
            'fields': (
                'views', 'created_at', 'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProjectFeatureInline, ProjectTechnologyInline]

@admin.register(ProjectStat)
class ProjectStatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label_ru', 'order']
    list_editable = ['order']

@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ['project', 'text_ru', 'order']
    list_filter = ['project']
    list_editable = ['order']

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'color', 'order']
    list_filter = ['project']
    list_editable = ['order']