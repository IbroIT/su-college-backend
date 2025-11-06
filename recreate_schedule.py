#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule
from datetime import date

# Очищаем старые расписания
Schedule.objects.all().delete()

# Получаем данные
try:
    group = StudyGroup.objects.get(name='CS-11-25')
    subject = Subject.objects.get(name_ru='Алгебра')
    teacher = Teacher.objects.get(first_name='Ибро')  # Изменено
    room = Room.objects.get(number='201', building='Главный')
    timeslot = TimeSlot.objects.get(number=1)  # 1 пара: 9:00-10:20
    
    # Создаем новое расписание
    schedule = Schedule.objects.create(
        group=group,
        subject=subject,
        teacher=teacher,
        room=room,
        time_slot=timeslot,
        weekday=5,  # Пятница
        lesson_type='lecture',
        week_type='both',
        start_date=date.today(),
        end_date=date(2025, 12, 31),
        is_active=True
    )
    
    print(f"Создано расписание: {schedule}")
    print(f"Группа: {group.name}")
    print(f"Предмет: {subject.name_ru}")
    print(f"Преподаватель: {teacher}")
    print(f"Аудитория: {room}")
    print(f"Время: {timeslot}")
    print(f"День: {schedule.get_weekday_display()}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    print("Проверьте, что все необходимые данные существуют в базе")