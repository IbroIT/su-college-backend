#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule
from datetime import date

# Создаем дополнительные группы одного курса
try:
    # Получаем или создаем группы 1 курса
    groups_1_course = []
    group_names = ['CS-11-25', 'CS-12-25', 'CS-13-25']
    
    for name in group_names:
        group, created = StudyGroup.objects.get_or_create(
            name=name,
            defaults={'is_active': True}
        )
        groups_1_course.append(group)
        if created:
            print(f"Создана группа: {name}")
        else:
            print(f"Группа уже существует: {name}")
    
    # Создаем преподавателя для поточной лекции
    teacher_math, created = Teacher.objects.get_or_create(
        first_name='Владимир',
        last_name='Иванов',
        defaults={
            'middle_name': 'Петрович',
            'is_active': True
        }
    )
    
    # Создаем предмет для поточной лекции
    higher_math, created = Subject.objects.get_or_create(
        name_ru='Высшая математика',
        defaults={
            'name_en': 'Higher Mathematics',
            'name_ky': 'Жогорку математика',
            'is_active': True
        }
    )
    
    # Создаем большую аудиторию для поточной лекции
    big_room, created = Room.objects.get_or_create(
        number='Актовый-зал',
        defaults={'is_active': True}
    )
    
    # Получаем временной слот
    timeslot_2 = TimeSlot.objects.get(number=2)  # 10:30-11:50
    
    print(f"\n=== Создаем поточную лекцию ===")
    print(f"Предмет: {higher_math.name_ru}")
    print(f"Преподаватель: {teacher_math}")
    print(f"Аудитория: {big_room}")
    print(f"Время: {timeslot_2}")
    print(f"День: Среда")
    print(f"Группы: {', '.join([g.name for g in groups_1_course])}")
    
    # Удаляем старые записи этой поточной лекции, если есть
    Schedule.objects.filter(
        subject=higher_math,
        teacher=teacher_math,
        time_slot=timeslot_2,
        weekday=3  # Среда
    ).delete()
    
    # Создаем одинаковое расписание для всех групп курса
    created_schedules = []
    for group in groups_1_course:
        schedule = Schedule.objects.create(
            group=group,
            subject=higher_math,
            teacher=teacher_math,
            room=big_room,
            time_slot=timeslot_2,
            weekday=3,  # Среда
            lesson_type='lecture',
            week_type='both',
            start_date=date.today(),
            end_date=date(2025, 12, 31),
            is_active=True,
            notes=f'Поточная лекция для 1 курса'
        )
        created_schedules.append(schedule)
        print(f"✓ Создано расписание для группы {group.name}")
    
    print(f"\n✅ Успешно создана поточная лекция для {len(created_schedules)} групп")
    
    # Создадим еще одну поточную лекцию - по физике
    print(f"\n=== Создаем вторую поточную лекцию ===")
    
    # Преподаватель физики для поточных лекций
    teacher_physics_stream, created = Teacher.objects.get_or_create(
        first_name='Наталья',
        last_name='Соколова',
        defaults={
            'middle_name': 'Викторовна',
            'is_active': True
        }
    )
    
    # Предмет физики
    physics_stream, created = Subject.objects.get_or_create(
        name_ru='Общая физика',
        defaults={
            'name_en': 'General Physics',
            'name_ky': 'Жалпы физика',
            'is_active': True
        }
    )
    
    # Лекционная аудитория
    lecture_hall, created = Room.objects.get_or_create(
        number='Лекц-зал-1',
        defaults={'is_active': True}
    )
    
    timeslot_1 = TimeSlot.objects.get(number=1)  # 9:00-10:20
    
    # Удаляем старые записи
    Schedule.objects.filter(
        subject=physics_stream,
        teacher=teacher_physics_stream,
        time_slot=timeslot_1,
        weekday=4  # Четверг
    ).delete()
    
    print(f"Предмет: {physics_stream.name_ru}")
    print(f"Преподаватель: {teacher_physics_stream}")
    print(f"Аудитория: {lecture_hall}")
    print(f"Время: {timeslot_1}")
    print(f"День: Четверг")
    
    # Создаем поточную лекцию по физике
    for group in groups_1_course:
        schedule = Schedule.objects.create(
            group=group,
            subject=physics_stream,
            teacher=teacher_physics_stream,
            room=lecture_hall,
            time_slot=timeslot_1,
            weekday=4,  # Четверг
            lesson_type='lecture',
            week_type='both',
            start_date=date.today(),
            end_date=date(2025, 12, 31),
            is_active=True,
            notes=f'Поточная лекция по физике для 1 курса'
        )
        print(f"✓ Создано расписание по физике для группы {group.name}")
    
    print(f"\n🎓 Поточные лекции созданы!")
    print(f"📚 Теперь группы {', '.join([g.name for g in groups_1_course])} имеют общие лекции:")
    print(f"   • Высшая математика - Среда, 2 пара - {teacher_math}")
    print(f"   • Общая физика - Четверг, 1 пара - {teacher_physics_stream}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()