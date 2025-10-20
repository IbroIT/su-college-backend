from django.contrib import admin
from .models import VacancyCategory, Vacancy, Benefit, VacancyStat, ApplicationInfo

@admin.register(VacancyCategory)
class VacancyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'icon', 'color', 'order']
    list_editable = ['order']

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'category', 'status', 'is_featured', 'is_urgent', 'order', 'deadline']
    list_filter = ['category', 'status', 'is_featured', 'is_urgent', 'created_at']
    list_editable = ['status', 'is_featured', 'is_urgent', 'order']
    search_fields = ['title_ru', 'title_kg', 'title_en', 'description_ru']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title_ru', 'title_kg', 'title_en',
                'description_ru', 'description_kg', 'description_en',
                'category'
            )
        }),
        ('Требования', {
            'fields': (
                'requirements_ru', 'requirements_kg', 'requirements_en',
            )
        }),
        ('Условия работы', {
            'fields': (
                'salary', 'work_schedule', 'employment_type',
            )
        }),
        ('Контактная информация', {
            'fields': (
                'contact_email', 'contact_person', 'contact_phone',
            )
        }),
        ('Настройки', {
            'fields': (
                'status', 'is_featured', 'is_urgent', 'order', 'deadline',
            )
        }),
    )

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'icon', 'order']
    list_editable = ['order']

@admin.register(VacancyStat)
class VacancyStatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label_ru', 'order']
    list_editable = ['order']

@admin.register(ApplicationInfo)
class ApplicationInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject_template_ru']
    
    def has_add_permission(self, request):
        # Разрешить только одну запись
        return not ApplicationInfo.objects.exists()