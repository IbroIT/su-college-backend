# -*- coding: utf-8 -*-
from datetime import time, date, timedelta
from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule

print("Creating test data for schedule...")

# Create time slots
time_slots_data = [
    (1, time(8, 30), time(10, 0)),
    (2, time(10, 10), time(11, 40)),
    (3, time(11, 50), time(13, 20)),
    (4, time(13, 30), time(15, 0)),
    (5, time(15, 10), time(16, 40)),
    (6, time(16, 50), time(18, 20))
]

for number, start_time, end_time in time_slots_data:
    TimeSlot.objects.get_or_create(
        number=number,
        defaults={
            'start_time': start_time,
            'end_time': end_time,
            'is_active': True
        }
    )

print("Time slots created")

# Create study groups
groups_data = [
    ("CS-101", 1, "Computer Science"),
    ("CS-102", 1, "Computer Science"),
    ("BUS-201", 2, "Business"),
    ("LAW-301", 3, "Law"),
    ("MED-401", 4, "Medicine"),
]

for name, course, faculty in groups_data:
    StudyGroup.objects.get_or_create(
        name=name,
        defaults={
            'course': course,
            'faculty': faculty,
            'is_active': True
        }
    )

print("Study groups created")

# Create subjects
subjects_data = [
    ("Mathematics", "Mathematics", "Mathematics", "MATH101", 4),
    ("Physics", "Physics", "Physics", "PHYS101", 3),
    ("Programming", "Programming", "Programming", "CS101", 5),
    ("English", "English", "English", "ENG101", 2),
    ("Economics", "Economics", "Economics", "ECON101", 3),
]

for name_ru, name_en, name_ky, code, credits in subjects_data:
    Subject.objects.get_or_create(
        code=code,
        defaults={
            'name_ru': name_ru,
            'name_en': name_en,
            'name_ky': name_ky,
            'credits': credits,
            'is_active': True
        }
    )

print("Subjects created")

# Create teachers
teachers_data = [
    ("John", "Smith", "Michael", "j.smith@college.kg", "Mathematics", "Professor"),
    ("Jane", "Doe", "Marie", "j.doe@college.kg", "Physics", "Associate Professor"),
    ("Bob", "Johnson", "Robert", "b.johnson@college.kg", "Computer Science", "Senior Lecturer"),
    ("Alice", "Brown", "Ann", "a.brown@college.kg", "Languages", "Lecturer"),
    ("Mike", "Wilson", "James", "m.wilson@college.kg", "Economics", "Associate Professor"),
]

for first_name, last_name, middle_name, email, department, position in teachers_data:
    Teacher.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'department': department,
            'position': position,
            'is_active': True
        }
    )

print("Teachers created")

# Create rooms
rooms_data = [
    ("101", "A", 1, 30, "lecture"),
    ("102", "A", 1, 25, "computer"),
    ("201", "A", 2, 35, "lecture"),
    ("202", "A", 2, 20, "computer"),
    ("301", "B", 3, 40, "lecture"),
]

for number, building, floor, capacity, room_type in rooms_data:
    Room.objects.get_or_create(
        number=number,
        building=building,
        defaults={
            'floor': floor,
            'capacity': capacity,
            'room_type': room_type,
            'is_active': True
        }
    )

print("Rooms created")

print("Test data successfully loaded!")