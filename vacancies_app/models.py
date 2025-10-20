from django.db import models
from django.utils.translation import gettext_lazy as _

class VacancyCategory(models.Model):
    name_ru = models.CharField(max_length=100, verbose_name=_("Название (русский)"))
    name_kg = models.CharField(max_length=100, verbose_name=_("Название (кыргызский)"))
    name_en = models.CharField(max_length=100, verbose_name=_("Название (английский)"))
    icon = models.CharField(max_length=50, verbose_name=_("Иконка"))
    color = models.CharField(max_length=100, default="from-blue-500 to-cyan-500", verbose_name=_("Цвет градиента"))
    bg_color = models.CharField(max_length=100, default="from-blue-50 to-cyan-50", verbose_name=_("Цвет фона"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Категория вакансий")
        verbose_name_plural = _("Категории вакансий")
        ordering = ['order']
    
    def __str__(self):
        return self.name_ru

class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('active', _('Активная')),
        ('closed', _('Закрытая')),
        ('draft', _('Черновик')),
    ]
    
    # Основная информация
    title_ru = models.CharField(max_length=200, verbose_name=_("Название (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Название (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Название (английский)"))
    
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    
    # Категория и тип
    category = models.ForeignKey(VacancyCategory, on_delete=models.CASCADE, related_name='vacancies', verbose_name=_("Категория"))
    
    # Требования
    requirements_ru = models.JSONField(default=list, verbose_name=_("Требования (русский)"))
    requirements_kg = models.JSONField(default=list, verbose_name=_("Требования (кыргызский)"))
    requirements_en = models.JSONField(default=list, verbose_name=_("Требования (английский)"))
    
    # Условия работы
    salary = models.CharField(max_length=100, blank=True, verbose_name=_("Зарплата"))
    work_schedule = models.CharField(max_length=100, blank=True, verbose_name=_("График работы"))
    employment_type = models.CharField(max_length=100, blank=True, verbose_name=_("Тип занятости"))
    
    # Контактная информация
    contact_email = models.EmailField(verbose_name=_("Контактный email"))
    contact_person = models.CharField(max_length=200, blank=True, verbose_name=_("Контактное лицо"))
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Контактный телефон"))
    
    # Метаданные
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name=_("Статус"))
    is_featured = models.BooleanField(default=False, verbose_name=_("В избранное"))
    is_urgent = models.BooleanField(default=False, verbose_name=_("Срочная"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    # Даты
    deadline = models.DateField(blank=True, null=True, verbose_name=_("Срок подачи"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Вакансия")
        verbose_name_plural = _("Вакансии")
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title_ru
    
    def is_active(self):
        return self.status == 'active'

class Benefit(models.Model):
    icon = models.CharField(max_length=50, verbose_name=_("Иконка"))
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (английский)"))
    description_ru = models.TextField(verbose_name=_("Описание (русский)"))
    description_kg = models.TextField(verbose_name=_("Описание (кыргызский)"))
    description_en = models.TextField(verbose_name=_("Описание (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Преимущество")
        verbose_name_plural = _("Преимущества")
        ordering = ['order']
    
    def __str__(self):
        return self.title_ru

class VacancyStat(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Число"))
    label_ru = models.CharField(max_length=100, verbose_name=_("Подпись (русский)"))
    label_kg = models.CharField(max_length=100, verbose_name=_("Подпись (кыргызский)"))
    label_en = models.CharField(max_length=100, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Статистика вакансий")
        verbose_name_plural = _("Статистика вакансий")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label_ru}"

class ApplicationInfo(models.Model):
    email = models.EmailField(verbose_name=_("Email для заявок"))
    subject_template_ru = models.CharField(max_length=200, verbose_name=_("Тема письма (русский)"))
    subject_template_kg = models.CharField(max_length=200, verbose_name=_("Тема письма (кыргызский)"))
    subject_template_en = models.CharField(max_length=200, verbose_name=_("Тема письма (английский)"))
    deadline_text_ru = models.CharField(max_length=200, verbose_name=_("Текст дедлайна (русский)"))
    deadline_text_kg = models.CharField(max_length=200, verbose_name=_("Текст дедлайна (кыргызский)"))
    deadline_text_en = models.CharField(max_length=200, verbose_name=_("Текст дедлайна (английский)"))
    documents_ru = models.JSONField(default=list, verbose_name=_("Документы (русский)"))
    documents_kg = models.JSONField(default=list, verbose_name=_("Документы (кыргызский)"))
    documents_en = models.JSONField(default=list, verbose_name=_("Документы (английский)"))
    
    class Meta:
        verbose_name = _("Информация о подаче заявки")
        verbose_name_plural = _("Информация о подаче заявки")
    
    def __str__(self):
        return "Информация о подаче заявок"