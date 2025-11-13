from django.db import models
from django.utils.translation import gettext_lazy as _

class ResourceCategory(models.Model):
    name_ru = models.CharField(max_length=100, verbose_name=_("Название (русский)"))
    name_kg = models.CharField(max_length=100, verbose_name=_("Название (кыргызский)"))
    name_en = models.CharField(max_length=100, verbose_name=_("Название (английский)"))
    icon = models.CharField(max_length=50, verbose_name=_("Иконка"))
    color = models.CharField(max_length=100, default="from-blue-500 to-cyan-500", verbose_name=_("Цвет градиента"))
    bg_color = models.CharField(max_length=100, default="from-blue-50 to-cyan-50", verbose_name=_("Цвет фона"))
    border_color = models.CharField(max_length=100, default="border-blue-200", verbose_name=_("Цвет бордера"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Категория ресурсов")
        verbose_name_plural = _("Категории ресурсов")
        ordering = ['order']
    
    def __str__(self):
        return self.name_ru

class EducationalResource(models.Model):
    ACCESS_TYPES = [
        ('physical', _('Физический доступ')),
        ('online', _('Онлайн доступ')),
        ('campus', _('Доступ в кампусе')),
        ('subscription', _('По подписке')),
    ]
    
    RESOURCE_TYPES = [
        ('paper', _('Бумажный')),
        ('electronic', _('Электронный')),
        ('mixed', _('Смешанный')),
    ]
    
    # Основная информация
    title_ru = models.CharField(max_length=200, verbose_name=_("Название (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Название (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Название (английский)"))
    
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    
    # Категория и тип
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources', verbose_name=_("Категория"))
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, verbose_name=_("Тип ресурса"))
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES, verbose_name=_("Тип доступа"))
    
    # Количественные данные
    count = models.CharField(max_length=50, verbose_name=_("Количество"))
    available_count = models.IntegerField(default=0, verbose_name=_("Доступное количество"))
    
    # Ссылки и файлы
    access_url = models.URLField(blank=True, verbose_name=_("Ссылка для доступа"))
    download_url = models.URLField(blank=True, verbose_name=_("Ссылка для скачивания"))
    document_file = models.FileField(upload_to='resources/documents/', blank=True, null=True, verbose_name=_("Файл документа"))
    
    # Метаданные
    is_featured = models.BooleanField(default=False, verbose_name=_("В избранное"))
    pinned = models.BooleanField(default=False, verbose_name=_("Закреплено"))
    is_available = models.BooleanField(default=True, verbose_name=_("Доступно"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    
    class Meta:
        verbose_name = _("Образовательный ресурс")
        verbose_name_plural = _("Образовательные ресурсы")
        ordering = ['order', 'category__order']
    
    def __str__(self):
        return self.title_ru
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class LibraryFeature(models.Model):
    icon = models.CharField(max_length=50, verbose_name=_("Иконка"))
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (английский)"))
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name=_("Цвет иконки"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Функция библиотеки")
        verbose_name_plural = _("Функции библиотеки")
        ordering = ['order']
    
    def __str__(self):
        return self.title_ru

class LibraryStat(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Число"))
    label_ru = models.CharField(max_length=100, verbose_name=_("Подпись (русский)"))
    label_kg = models.CharField(max_length=100, verbose_name=_("Подпись (кыргызский)"))
    label_en = models.CharField(max_length=100, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Статистика библиотеки")
        verbose_name_plural = _("Статистика библиотеки")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label_ru}"

class WorkingHours(models.Model):
    day_ru = models.CharField(max_length=50, verbose_name=_("День (русский)"))
    day_kg = models.CharField(max_length=50, verbose_name=_("День (кыргызский)"))
    day_en = models.CharField(max_length=50, verbose_name=_("День (английский)"))
    time_ru = models.CharField(max_length=50, verbose_name=_("Время (русский)"))
    time_kg = models.CharField(max_length=50, verbose_name=_("Время (кыргызский)"))
    time_en = models.CharField(max_length=50, verbose_name=_("Время (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Часы работы")
        verbose_name_plural = _("Часы работы")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.day_ru} - {self.time_ru}"