from django.db import models
from django.utils.translation import gettext_lazy as _

class StudyGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Название группы"))
    full_name_ru = models.CharField(max_length=200, verbose_name=_("Полное название (русский)"))
    full_name_kg = models.CharField(max_length=200, verbose_name=_("Полное название (кыргызский)"))
    full_name_en = models.CharField(max_length=200, verbose_name=_("Полное название (английский)"))
    course = models.IntegerField(verbose_name=_("Курс"))
    department = models.CharField(max_length=100, verbose_name=_("Факультет"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активная"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Учебная группа")
        verbose_name_plural = _("Учебные группы")
        ordering = ['course', 'name']
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name_ru = models.CharField(max_length=200, verbose_name=_("ФИО (русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("ФИО (кыргызский)"))
    name_en = models.CharField(max_length=200, verbose_name=_("ФИО (английский)"))
    position_ru = models.CharField(max_length=100, verbose_name=_("Должность (русский)"))
    position_kg = models.CharField(max_length=100, verbose_name=_("Должность (кыргызский)"))
    position_en = models.CharField(max_length=100, verbose_name=_("Должность (английский)"))
    department = models.CharField(max_length=100, verbose_name=_("Кафедра"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Телефон"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    
    class Meta:
        verbose_name = _("Преподаватель")
        verbose_name_plural = _("Преподаватели")
    
    def __str__(self):
        return self.name_ru

class Classroom(models.Model):
    number = models.CharField(max_length=20, verbose_name=_("Номер аудитории"))
    building = models.CharField(max_length=50, verbose_name=_("Корпус"))
    capacity = models.IntegerField(verbose_name=_("Вместимость"))
    room_type_ru = models.CharField(max_length=100, verbose_name=_("Тип аудитории (русский)"))
    room_type_kg = models.CharField(max_length=100, verbose_name=_("Тип аудитории (кыргызский)"))
    room_type_en = models.CharField(max_length=100, verbose_name=_("Тип аудитории (английский)"))
    equipment = models.TextField(blank=True, verbose_name=_("Оборудование"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активная"))
    
    class Meta:
        verbose_name = _("Аудитория")
        verbose_name_plural = _("Аудитории")
    
    def __str__(self):
        return f"{self.building}-{self.number}"

class Subject(models.Model):
    name_ru = models.CharField(max_length=200, verbose_name=_("Название (русский)"))
    name_kg = models.CharField(max_length=200, verbose_name=_("Название (кыргызский)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Название (английский)"))
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Код предмета"))
    credits = models.IntegerField(verbose_name=_("Кредиты"))
    hours_total = models.IntegerField(verbose_name=_("Всего часов"))
    hours_lecture = models.IntegerField(default=0, verbose_name=_("Лекционные часы"))
    hours_practice = models.IntegerField(default=0, verbose_name=_("Практические часы"))
    hours_lab = models.IntegerField(default=0, verbose_name=_("Лабораторные часы"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    
    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")
    
    def __str__(self):
        return self.name_ru

class LessonType(models.Model):
    name_ru = models.CharField(max_length=50, verbose_name=_("Название (русский)"))
    name_kg = models.CharField(max_length=50, verbose_name=_("Название (кыргызский)"))
    name_en = models.CharField(max_length=50, verbose_name=_("Название (английский)"))
    color = models.CharField(max_length=100, default="from-blue-500 to-cyan-500", verbose_name=_("Цвет градиента"))
    short_name_ru = models.CharField(max_length=10, verbose_name=_("Короткое название (русский)"))
    short_name_kg = models.CharField(max_length=10, verbose_name=_("Короткое название (кыргызский)"))
    short_name_en = models.CharField(max_length=10, verbose_name=_("Короткое название (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Тип занятия")
        verbose_name_plural = _("Типы занятий")
        ordering = ['order']
    
    def __str__(self):
        return self.name_ru

class TimeSlot(models.Model):
    number = models.IntegerField(unique=True, verbose_name=_("Номер пары"))
    start_time = models.TimeField(verbose_name=_("Время начала"))
    end_time = models.TimeField(verbose_name=_("Время окончания"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Временной слот")
        verbose_name_plural = _("Временные слоты")
        ordering = ['number']
    
    def __str__(self):
        return f"Пара {self.number} ({self.start_time} - {self.end_time})"

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (0, _('Понедельник')),
        (1, _('Вторник')),
        (2, _('Среда')),
        (3, _('Четверг')),
        (4, _('Пятница')),
        (5, _('Суббота')),
        (6, _('Воскресенье')),
    ]
    
    WEEK_TYPES = [
        ('both', _('Обе недели')),
        ('numerator', _('Числитель')),
        ('denominator', _('Знаменатель')),
    ]
    
    # Основная информация
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name=_("День недели"))
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name=_("Временной слот"))
    week_type = models.CharField(max_length=15, choices=WEEK_TYPES, default='both', verbose_name=_("Тип недели"))  # Изменено с 10 на 15
    
    # Связи
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Предмет"))
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=_("Преподаватель"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_("Аудитория"))
    groups = models.ManyToManyField(StudyGroup, verbose_name=_("Группы"))
    lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE, verbose_name=_("Тип занятия"))
    
    # Дополнительная информация
    subgroup = models.CharField(max_length=10, blank=True, verbose_name=_("Подгруппа"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активное"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    # Даты
    start_date = models.DateField(verbose_name=_("Дата начала"))
    end_date = models.DateField(verbose_name=_("Дата окончания"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Расписание")
        verbose_name_plural = _("Расписание")
        ordering = ['day_of_week', 'time_slot__number', 'order']
    
    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.time_slot} - {self.subject}"

class ScheduleFeature(models.Model):
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
        verbose_name = _("Особенность расписания")
        verbose_name_plural = _("Особенности расписания")
        ordering = ['order']
    
    def __str__(self):
        return self.title_ru

class ScheduleStat(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Число"))
    label_ru = models.CharField(max_length=100, verbose_name=_("Подпись (русский)"))
    label_kg = models.CharField(max_length=100, verbose_name=_("Подпись (кыргызский)"))
    label_en = models.CharField(max_length=100, verbose_name=_("Подпись (английский)"))
    order = models.IntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        verbose_name = _("Статистика расписания")
        verbose_name_plural = _("Статистика расписания")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.number} - {self.label_ru}"