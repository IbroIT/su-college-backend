from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class StudyGroup(models.Model):
    """Модель для учебных групп"""
    name = models.CharField(max_length=50, verbose_name=_("Название группы"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))
    
    class Meta:
        verbose_name = _("Учебная группа")
        verbose_name_plural = _("Учебные группы")
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Subject(models.Model):
    """Модель для предметов с поддержкой многоязычности"""
    name_ru = models.CharField(max_length=200, verbose_name=_("Название (Русский)"))
    name_en = models.CharField(max_length=200, verbose_name=_("Название (English)"))
    name_ky = models.CharField(max_length=200, verbose_name=_("Название (Кыргызча)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    
    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")
        ordering = ['name_ru']
        
    def __str__(self):
        return self.name_ru


class Teacher(models.Model):
    """Модель для преподавателей"""
    first_name = models.CharField(max_length=100, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=100, verbose_name=_("Фамилия"))
    middle_name = models.CharField(max_length=100, blank=True, verbose_name=_("Отчество"))
    subjects = models.ManyToManyField(Subject, verbose_name=_("Предметы"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    
    class Meta:
        verbose_name = _("Преподаватель")
        verbose_name_plural = _("Преподаватели")
        ordering = ['last_name', 'first_name']
        
    def __str__(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0]}."
        return f"{self.last_name} {self.first_name[0]}."
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Room(models.Model):
    """Модель для аудиторий"""
    number = models.CharField(max_length=20, unique=True, verbose_name=_("Номер аудитории"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))
    
    class Meta:
        verbose_name = _("Аудитория")
        verbose_name_plural = _("Аудитории")
        ordering = ['number']
        
    def __str__(self):
        return self.number


class TimeSlot(models.Model):
    """Модель для временных слотов"""
    number = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name=_("Номер пары")
    )
    start_time = models.TimeField(verbose_name=_("Время начала"))
    end_time = models.TimeField(verbose_name=_("Время окончания"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))
    
    class Meta:
        verbose_name = _("Временной слот")
        verbose_name_plural = _("Временные слоты")
        ordering = ['number']
        
    def __str__(self):
        start_time_str = self.start_time.strftime('%H:%M')
        end_time_str = self.end_time.strftime('%H:%M')
        return f"{self.number} пара ({start_time_str} - {end_time_str})"


class Schedule(models.Model):
    """Основная модель расписания"""
    WEEKDAYS = [
        (1, _('Понедельник')),
        (2, _('Вторник')),
        (3, _('Среда')),
        (4, _('Четверг')),
        (5, _('Пятница')),
        (6, _('Суббота')),
        (7, _('Воскресенье')),
    ]
    
    LESSON_TYPES = [
        ('lecture', _('Лекция')),
        ('practice', _('Практика')),
        ('lab', _('Лабораторная')),
        ('seminar', _('Семинар')),
        ('exam', _('Экзамен')),
        ('module', _('Модуль')),
        ('consultation', _('Консультация')),
        ('project', _('Проектная работа')),
        ('elective', _('Элективный курс')),
        ('club', _('Кружок')),
        ('sports', _('Спорт')),
    ]
    
    group = models.ForeignKey(
        StudyGroup, 
        on_delete=models.CASCADE, 
        verbose_name=_("Группа")
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        verbose_name=_("Предмет")
    )
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE, 
        verbose_name=_("Преподаватель")
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        verbose_name=_("Аудитория")
    )
    time_slot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.CASCADE, 
        verbose_name=_("Время")
    )
    weekday = models.IntegerField(
        choices=WEEKDAYS, 
        verbose_name=_("День недели")
    )
    lesson_type = models.CharField(
        max_length=20, 
        choices=LESSON_TYPES, 
        default='lecture',
        verbose_name=_("Тип занятия")
    )
    week_type = models.CharField(
        max_length=10,
        choices=[
            ('all', _('Каждую неделю')),
            ('odd', _('Нечетная неделя')),
            ('even', _('Четная неделя')),
        ],
        default='all',
        verbose_name=_("Тип недели")
    )
    start_date = models.DateField(verbose_name=_("Дата начала"), default='2024-01-01')
    end_date = models.DateField(verbose_name=_("Дата окончания"), default='2024-12-31')
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))
    notes = models.TextField(blank=True, verbose_name=_("Примечания"))
    
    class Meta:
        verbose_name = _("Расписание")
        verbose_name_plural = _("Расписание")
        ordering = ['weekday', 'time_slot__number']
        unique_together = [
            ['group', 'weekday', 'time_slot', 'start_date', 'end_date'],
            # Убираем ограничения для teacher и room - разрешаем поточные лекции
            # ['teacher', 'weekday', 'time_slot', 'start_date', 'end_date'],
            # ['room', 'weekday', 'time_slot', 'start_date', 'end_date'],
        ]
        
    def __str__(self):
        return f"{self.group.name} - {self.subject.name_ru} ({self.get_weekday_display()}, {self.time_slot.number} пара)"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.start_date > self.end_date:
            raise ValidationError(_("Дата начала не может быть позже даты окончания"))
            
        # Проверка на конфликты расписания
        conflicts = Schedule.objects.filter(
            weekday=self.weekday,
            time_slot=self.time_slot,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
            is_active=True
        ).exclude(pk=self.pk)
        
        # НЕ проверяем конфликт преподавателя - разрешаем поточные лекции
        # teacher_conflict = conflicts.filter(teacher=self.teacher)
        # if teacher_conflict.exists():
        #     raise ValidationError(
        #         _("Преподаватель %(teacher)s уже занят в это время") % {
        #             'teacher': self.teacher
        #         }
        #     )
        
        # НЕ проверяем конфликт аудитории - разрешаем поточные лекции
        # room_conflict = conflicts.filter(room=self.room)
        # if room_conflict.exists():
        #     raise ValidationError(
        #         _("Аудитория %(room)s уже занята в это время") % {
        #             'room': self.room
        #         }
        #     )
        
        # Проверка конфликта группы - группа не может быть в двух местах одновременно
        group_conflict = conflicts.filter(group=self.group)
        if group_conflict.exists():
            raise ValidationError(
                _("Группа %(group)s уже имеет занятие в это время") % {
                    'group': self.group
                }
            )


class ScheduleChange(models.Model):
    """Модель для изменений в расписании (переносы, отмены)"""
    CHANGE_TYPES = [
        ('cancel', _('Отмена')),
        ('reschedule', _('Перенос')),
        ('substitute', _('Замена преподавателя')),
        ('room_change', _('Смена аудитории')),
    ]
    
    original_schedule = models.ForeignKey(
        Schedule, 
        on_delete=models.CASCADE, 
        verbose_name=_("Оригинальное расписание")
    )
    change_type = models.CharField(
        max_length=20, 
        choices=CHANGE_TYPES, 
        verbose_name=_("Тип изменения")
    )
    change_date = models.DateField(verbose_name=_("Дата изменения"))
    new_teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=_("Новый преподаватель")
    )
    new_room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=_("Новая аудитория")
    )
    new_time_slot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=_("Новое время")
    )
    reason = models.TextField(verbose_name=_("Причина изменения"))
    created_by = models.CharField(max_length=100, verbose_name=_("Кем создано"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    class Meta:
        verbose_name = _("Изменение расписания")
        verbose_name_plural = _("Изменения расписания")
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_change_type_display()} - {self.original_schedule} ({self.change_date})"