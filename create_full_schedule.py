#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule
from datetime import date

# Получаем данные
try:
    group = StudyGroup.objects.get(name='CS-11-25')
    
    # Создаем дополнительные предметы
    physics, created = Subject.objects.get_or_create(
        name_ru='Физика',
        defaults={
            'name_en': 'Physics',
            'name_ky': 'Физика',
            'is_active': True
        }
    )
    
    programming, created = Subject.objects.get_or_create(
        name_ru='Программирование',
        defaults={
            'name_en': 'Programming',
            'name_ky': 'Программалоо',
            'is_active': True
        }
    )
    
    english, created = Subject.objects.get_or_create(
        name_ru='Английский язык',
        defaults={
            'name_en': 'English Language',
            'name_ky': 'Англис тили',
            'is_active': True
        }
    )
    
    # Создаем дополнительных преподавателей
    teacher_physics, created = Teacher.objects.get_or_create(
        first_name='Анна',
        last_name='Петрова',
        defaults={
            'middle_name': 'Ивановна',
            'is_active': True
        }
    )
    
    teacher_programming, created = Teacher.objects.get_or_create(
        first_name='Максим',
        last_name='Смирнов',
        defaults={
            'middle_name': 'Александрович',
            'is_active': True
        }
    )
    
    teacher_english, created = Teacher.objects.get_or_create(
        first_name='Елена',
        last_name='Козлова',
        defaults={
            'middle_name': 'Сергеевна',
            'is_active': True
        }
    )
    
    # Создаем дополнительные аудитории
    room_102, created = Room.objects.get_or_create(
        number='A-102',
        defaults={'is_active': True}
    )
    
    room_lab, created = Room.objects.get_or_create(
        number='Лаб-301',
        defaults={'is_active': True}
    )
    
    room_203, created = Room.objects.get_or_create(
        number='A-203',
        defaults={'is_active': True}
    )
    
    # Получаем временные слоты
    timeslot_1 = TimeSlot.objects.get(number=1)  # 9:00-10:20
    timeslot_2 = TimeSlot.objects.get(number=2)  # 10:30-11:50
    timeslot_3 = TimeSlot.objects.get(number=3)  # 12:00-13:20
    timeslot_4 = TimeSlot.objects.get(number=4)  # 14:00-15:20
    
    # Очищаем старые расписания для этой группы
    Schedule.objects.filter(group=group).delete()
    
    # Создаем расписание на неделю
    schedules_to_create = [
        # Понедельник
        {
            'group': group, 'subject': programming, 'teacher': teacher_programming,
            'room': room_lab, 'time_slot': timeslot_1, 'weekday': 1,
            'lesson_type': 'lab', 'week_type': 'both'
        },
        {
            'group': group, 'subject': physics, 'teacher': teacher_physics,
            'room': room_102, 'time_slot': timeslot_2, 'weekday': 1,
            'lesson_type': 'lecture', 'week_type': 'both'
        },
        
        # Вторник  
        {
            'group': group, 'subject': english, 'teacher': teacher_english,
            'room': room_203, 'time_slot': timeslot_1, 'weekday': 2,
            'lesson_type': 'practice', 'week_type': 'both'
        },
        {
            'group': group, 'subject': programming, 'teacher': teacher_programming,
            'room': room_lab, 'time_slot': timeslot_3, 'weekday': 2,
            'lesson_type': 'practice', 'week_type': 'both'
        },
        
        # Среда
        {
            'group': group, 'subject': physics, 'teacher': teacher_physics,
            'room': room_102, 'time_slot': timeslot_1, 'weekday': 3,
            'lesson_type': 'practice', 'week_type': 'both'
        },
        
        # Четверг
        {
            'group': group, 'subject': english, 'teacher': teacher_english,
            'room': room_203, 'time_slot': timeslot_2, 'weekday': 4,
            'lesson_type': 'lecture', 'week_type': 'both'
        },
        {
            'group': group, 'subject': programming, 'teacher': teacher_programming,
            'room': room_lab, 'time_slot': timeslot_4, 'weekday': 4,
            'lesson_type': 'lab', 'week_type': 'both'
        },
        
        # Пятница (оставляем алгебру)
        {
            'group': group, 'subject': Subject.objects.get(name_ru='Алгебра'),
            'teacher': Teacher.objects.get(first_name='Ибро'),
            'room': Room.objects.get(number='Главный-201'),
            'time_slot': timeslot_1, 'weekday': 5,
            'lesson_type': 'lecture', 'week_type': 'both'
        },
        {
            'group': group, 'subject': physics, 'teacher': teacher_physics,
            'room': room_102, 'time_slot': timeslot_3, 'weekday': 5,
            'lesson_type': 'lab', 'week_type': 'both'
        },
    ]
    
    # Создаем все расписания
    for schedule_data in schedules_to_create:
        schedule = Schedule.objects.create(
            **schedule_data,
            start_date=date.today(),
            end_date=date(2025, 12, 31),
            is_active=True
        )
        
        weekday_names = {
            1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 
            4: 'Четверг', 5: 'Пятница', 6: 'Суббота'
        }
        
        print(f"Создано: {weekday_names[schedule.weekday]} - {schedule.subject.name_ru} ({schedule.time_slot.number} пара)")
    
    print(f"\nУспешно создано {len(schedules_to_create)} записей расписания для группы {group.name}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()