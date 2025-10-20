from django.db import models
from django.utils.translation import gettext_lazy as _

class Teacher(models.Model):
    name_ru = models.CharField(max_length=200, verbose_name=_("Имя (русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Имя (кыргызский)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Имя (английский)"))
    
    subject_ru = models.CharField(max_length=200, verbose_name=_("Предмет (русский)"))
    subject_kg = models.CharField(max_length=200, verbose_name=_("Предмет (кыргызский)"))
    subject_en = models.CharField(max_length=200, verbose_name=_("Предмет (английский)"))
    
    image = models.ImageField(upload_to='teachers/', verbose_name=_("Фото"), blank=True, null=True)
    experience_ru = models.CharField(max_length=100, verbose_name=_("Опыт (русский)"))
    experience_kg = models.CharField(max_length=100, verbose_name=_("Опыт (кыргызский)"))
    experience_en = models.CharField(max_length=100, verbose_name=_("Опыт (английский)"))
    
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    
    rating = models.FloatField(default=0.0, verbose_name=_("Рейтинг"))
    color = models.CharField(
        max_length=100, 
        default="from-blue-500 to-cyan-500",
        verbose_name=_("Цвет градиента"),
        help_text=_("Например: from-blue-500 to-cyan-500")
    )
    
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок отображения"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Преподаватель")
        verbose_name_plural = _("Преподаватели")
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.name_ru

class Achievement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='achievements')
    text_ru = models.TextField(verbose_name=_("Достижение (русский)"))
    text_kg = models.TextField(verbose_name=_("Достижение (кыргызский)"))
    text_en = models.TextField(verbose_name=_("Достижение (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Достижение")
        verbose_name_plural = _("Достижения")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.teacher.name_ru} - {self.text_ru[:50]}"