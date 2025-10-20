from django.db import models
from django.utils.translation import gettext_lazy as _

class StudentProject(models.Model):
    # Основная информация
    student_name_ru = models.CharField(max_length=200, verbose_name=_("Имя студента (русский)"))
    student_name_kg = models.CharField(max_length=200, verbose_name=_("Имя студента (кыргызский)"))
    student_name_en = models.CharField(max_length=200, verbose_name=_("Имя студента (английский)"))
    
    title_ru = models.CharField(max_length=200, verbose_name=_("Название проекта (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Название проекта (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Название проекта (английский)"))
    
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    
    # Медиа
    student_image = models.ImageField(upload_to='projects/students/', blank=True, null=True, verbose_name=_("Скриншот проекта"))
    project_image = models.ImageField(upload_to='projects/screenshots/', blank=True, null=True, verbose_name=_("Игнор"))
    
    # Ссылки
    github_url = models.URLField(verbose_name=_("GitHub репозиторий"))
    website_url = models.URLField(blank=True, verbose_name=_("Вебсайт проекта"))
    demo_url = models.URLField(blank=True, verbose_name=_("Демо ссылка"))
    
    # Метаданные
    is_featured = models.BooleanField(default=False, verbose_name=_("В избранное"))
    is_published = models.BooleanField(default=True, verbose_name=_("Опубликовано"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок отображения"))
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    
    class Meta:
        verbose_name = _("Студенческий проект")
        verbose_name_plural = _("Студенческие проекты")
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.student_name_ru} - {self.title_ru}"
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class ProjectFeature(models.Model):
    project = models.ForeignKey(StudentProject, on_delete=models.CASCADE, related_name='features')
    text_ru = models.CharField(max_length=200, verbose_name=_("Особенность (русский)"))
    text_kg = models.CharField(max_length=200, verbose_name=_("Особенность (кыргызский)"))
    text_en = models.CharField(max_length=200, verbose_name=_("Особенность (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Особенность проекта")
        verbose_name_plural = _("Особенности проекта")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title_ru} - {self.text_ru}"

class ProjectTechnology(models.Model):
    project = models.ForeignKey(StudentProject, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=50, verbose_name=_("Название технологии"))
    icon = models.CharField(max_length=50, blank=True, verbose_name=_("Иконка"))
    color = models.CharField(max_length=100, default="from-blue-500 to-cyan-500", verbose_name=_("Цвет градиента"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Технология проекта")
        verbose_name_plural = _("Технологии проекта")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title_ru} - {self.name}"

class ProjectStat(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Число"))
    label_ru = models.CharField(max_length=100, verbose_name=_("Подпись (русский)"))
    label_kg = models.CharField(max_length=100, verbose_name=_("Подпись (кыргызский)"))
    label_en = models.CharField(max_length=100, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Статистика проектов")
        verbose_name_plural = _("Статистика проектов")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label_ru}"