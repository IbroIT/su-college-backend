from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Category(models.Model):
    name_ru = models.CharField(max_length=100, verbose_name=_("Название (русский)"))
    name_kg = models.CharField(max_length=100, verbose_name=_("Название (кыргызский)"))
    name_en = models.CharField(max_length=100, verbose_name=_("Название (английский)"))
    slug = models.SlugField(unique=True, verbose_name=_("URL"))
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name=_("Цвет"))
    
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
    
    def __str__(self):
        return self.name_ru

class News(models.Model):
    # Основная информация
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (английский)"))
    
    excerpt_ru = models.TextField(max_length=500, verbose_name=_("Краткое описание (русский)"))
    excerpt_kg = models.TextField(max_length=500, verbose_name=_("Краткое описание (кыргызский)"))
    excerpt_en = models.TextField(max_length=500, verbose_name=_("Краткое описание (английский)"))
    
    content_ru = models.TextField(verbose_name=_("Полный текст (русский)"))
    content_kg = models.TextField(verbose_name=_("Полный текст (кыргызский)"))
    content_en = models.TextField(verbose_name=_("Полный текст (английский)"))
    
    # Медиа
    image = models.ImageField(upload_to='news/', verbose_name=_("Главное изображение"))
    image_thumbnail = models.ImageField(upload_to='news/thumbnails/', blank=True, null=True, verbose_name=_("Миниатюра"))
    
    # Метаданные
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='news', verbose_name=_("Категория"))
    date = models.DateTimeField(verbose_name=_("Дата публикации"))
    is_featured = models.BooleanField(default=False, verbose_name=_("В избранное"))
    pinned = models.BooleanField(default=False, verbose_name=_("Закреплено"))
    is_published = models.BooleanField(default=True, verbose_name=_("Опубликовано"))
    slug = models.SlugField(unique=True, verbose_name=_("URL"))
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    
    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ['-pinned', '-date', '-created_at']
    
    def __str__(self):
        return self.title_ru
    
    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/gallery/')
    caption_ru = models.CharField(max_length=200, blank=True, verbose_name=_("Подпись (русский)"))
    caption_kg = models.CharField(max_length=200, blank=True, verbose_name=_("Подпись (кыргызский)"))
    caption_en = models.CharField(max_length=200, blank=True, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.news.title_ru}"