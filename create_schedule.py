# -*- coding: utf-8 -*-
from datetime import date, timedelta
from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule

print("Creating schedule entries...")

# Get existing objects
try:
    cs101 = StudyGroup.objects.get(name="CS-101")
    cs102 = StudyGroup.objects.get(name="CS-102")
    
    math_subject = Subject.objects.get(code="MATH101")
    physics_subject = Subject.objects.get(code="PHYS101")
    programming_subject = Subject.objects.get(code="CS101")
    
    teacher_smith = Teacher.objects.get(email="j.smith@college.kg")
    teacher_doe = Teacher.objects.get(email="j.doe@college.kg")
    teacher_johnson = Teacher.objects.get(email="b.johnson@college.kg")
    
    room_101 = Room.objects.get(number="101", building="A")
    room_102 = Room.objects.get(number="102", building="A")
    room_201 = Room.objects.get(number="201", building="A")
    
    slot_1 = TimeSlot.objects.get(number=1)
    slot_2 = TimeSlot.objects.get(number=2)
    slot_3 = TimeSlot.objects.get(number=3)
    
    # Create schedule for next 4 months
    today = date.today()
    start_date = today - timedelta(days=today.weekday())  # Monday
    end_date = start_date + timedelta(days=120)
    
    # Monday schedules
    Schedule.objects.get_or_create(
        group=cs101,
        subject=math_subject,
        teacher=teacher_smith,
        room=room_101,
        time_slot=slot_1,
        weekday=1,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'lesson_type': 'lecture',
            'week_type': 'all',
            'is_active': True,
            'notes': 'Mathematics for CS-101'
        }
    )
    
    Schedule.objects.get_or_create(
        group=cs102,
        subject=physics_subject,
        teacher=teacher_doe,
        room=room_201,
        time_slot=slot_1,
        weekday=1,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'lesson_type': 'lecture',
            'week_type': 'all',
            'is_active': True,
            'notes': 'Physics for CS-102'
        }
    )
    
    Schedule.objects.get_or_create(
        group=cs101,
        subject=programming_subject,
        teacher=teacher_johnson,
        room=room_102,
        time_slot=slot_2,
        weekday=1,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'lesson_type': 'practice',
            'week_type': 'all',
            'is_active': True,
            'notes': 'Programming practice for CS-101'
        }
    )
    
    # Tuesday schedules
    Schedule.objects.get_or_create(
        group=cs101,
        subject=physics_subject,
        teacher=teacher_doe,
        room=room_201,
        time_slot=slot_1,
        weekday=2,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'lesson_type': 'lecture',
            'week_type': 'all',
            'is_active': True,
            'notes': 'Physics for CS-101'
        }
    )
    
    Schedule.objects.get_or_create(
        group=cs102,
        subject=math_subject,
        teacher=teacher_smith,
        room=room_101,
        time_slot=slot_2,
        weekday=2,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'lesson_type': 'lecture',
            'week_type': 'all',
            'is_active': True,
            'notes': 'Mathematics for CS-102'
        }
    )
    
    print("Schedule entries created successfully!")
    print(f"Total schedules in database: {Schedule.objects.count()}")
    
except Exception as e:
    print(f"Error creating schedule entries: {e}")
    print("Make sure all required data exists (groups, subjects, teachers, rooms, time slots)")