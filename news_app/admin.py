from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import Category, News, NewsImage

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3
    fields = ['image', 'caption_ru', 'caption_kg', 'caption_en', 'order']

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name_ru', 'name_kg', 'name_en', 'slug', 'color_display']
    list_editable = ['slug']
    prepopulated_fields = {'slug': ('name_ru',)}
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">■</span> {}',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Цвет'

@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = [
        'title_ru', 
        'category', 
        'date', 
        'is_featured',
        'pinned',
        'is_published',
        'views',
        'created_at'
    ]
    list_filter = ['category', 'is_featured', 'pinned', 'is_published', 'date', 'created_at']
    list_editable = ['is_featured', 'pinned', 'is_published']
    search_fields = ['title_ru', 'title_kg', 'title_en', 'excerpt_ru']
    prepopulated_fields = {'slug': ('title_ru',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'is_featured',
                'is_published',
                'category',
                'date',
            )
        }),
        ('Русская версия', {
            'fields': (
                'title_ru',
                'excerpt_ru',
                'content_ru',
            )
        }),
        ('Кыргызская версия', {
            'fields': (
                'title_kg',
                'excerpt_kg', 
                'content_kg',
            )
        }),
        ('Английская версия', {
            'fields': (
                'title_en',
                'excerpt_en',
                'content_en',
            )
        }),
        ('Медиа и URL', {
            'fields': (
                'image',
                'slug',
            )
        }),
        ('Статистика', {
            'fields': (
                'views',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [NewsImageInline]

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['news', 'image', 'order']
    list_filter = ['news']
    list_editable = ['order']