from django.db import models
from django.utils.translation import gettext_lazy as _

class CouncilFeature(models.Model):
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
        verbose_name = _("Функция совета")
        verbose_name_plural = _("Функции совета")
        ordering = ['order']
    
    def __str__(self):
        return self.title_ru

class CouncilMember(models.Model):
    POSITION_CHOICES = [
        ('president', _('Президент')),
        ('vice_president', _('Вице-президент')),
        ('academic_manager', _('Академический менеджер')),
        ('event_manager', _('Менеджер мероприятий')),
        ('pr_manager', _('PR менеджер')),
        ('sports_manager', _('Спортивный менеджер')),
        ('other', _('Другое')),
    ]
    
    name_ru = models.CharField(max_length=200, verbose_name=_("Имя (русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Имя (кыргызский)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Имя (английский)"))
    
    position_ru = models.CharField(max_length=200, verbose_name=_("Должность (русский)"))
    position_kg = models.CharField(max_length=200, verbose_name=_("Должность (кыргызский)"))
    position_en = models.CharField(max_length=200, verbose_name=_("Должность (английский)"))
    
    bio_ru = models.TextField(verbose_name=_("Биография (русский)"))
    bio_kg = models.TextField(verbose_name=_("Биография (кыргызский)"))
    bio_en = models.TextField(verbose_name=_("Биография (английский)"))
    
    image = models.ImageField(upload_to='council/members/', blank=True, null=True, verbose_name=_("Фото"))
    position_type = models.CharField(max_length=50, choices=POSITION_CHOICES, default='other', verbose_name=_("Тип должности"))
    
    instagram = models.CharField(max_length=100, blank=True, verbose_name=_("Instagram"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    linkedin = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Член совета")
        verbose_name_plural = _("Члены совета")
        ordering = ['order', 'position_type']
    
    def __str__(self):
        return f"{self.name_ru} - {self.position_ru}"

class CouncilEvent(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name=_("Название (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Название (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Название (английский)"))
    
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    
    date = models.DateTimeField(verbose_name=_("Дата мероприятия"))
    participants = models.IntegerField(default=0, verbose_name=_("Количество участников"))
    location = models.CharField(max_length=200, blank=True, verbose_name=_("Место проведения"))
    
    is_active = models.BooleanField(default=True, verbose_name=_("Активное"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Мероприятие")
        verbose_name_plural = _("Мероприятия")
        ordering = ['date', 'order']
    
    def __str__(self):
        return self.title_ru

class CouncilStat(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Число"))
    label_ru = models.CharField(max_length=100, verbose_name=_("Подпись (русский)"))
    label_kg = models.CharField(max_length=100, verbose_name=_("Подпись (кыргызский)"))
    label_en = models.CharField(max_length=100, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Статистика")
        verbose_name_plural = _("Статистика")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label_ru}"