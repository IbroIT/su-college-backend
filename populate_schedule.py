"""
Скрипт для заполнения базы данных тестовыми данными расписания
Запуск: python manage.py shell < populate_schedule.py
"""

from datetime import time, date, timedelta
from schedule_app.models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule

def create_test_data():
    print("Создание тестовых данных для расписания...")
    
    # Создаем временные слоты
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
    
    print("Временные слоты созданы")
    
    # Создаем учебные группы
    groups_data = [
        ("CS-101", 1, "Компьютерные науки"),
        ("CS-102", 1, "Компьютерные науки"),
        ("BUS-201", 2, "Бизнес"),
        ("LAW-301", 3, "Юриспруденция"),
        ("MED-401", 4, "Медицина"),
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
    
    print("Учебные группы созданы")
    
    # Создаем предметы
    subjects_data = [
        ("Математика", "Mathematics", "Математика", "MATH101", 4),
        ("Физика", "Physics", "Физика", "PHYS101", 3),
        ("Программирование", "Programming", "Программалоо", "CS101", 5),
        ("Английский язык", "English", "Англис тили", "ENG101", 2),
        ("Экономика", "Economics", "Экономика", "ECON101", 3),
        ("Базы данных", "Databases", "Маалымат базасы", "CS201", 4),
        ("Веб-разработка", "Web Development", "Веб иштетүү", "CS301", 4),
        ("Алгоритмы", "Algorithms", "Алгоритмдер", "CS401", 5),
        ("Сети", "Networks", "Тармактар", "CS501", 3),
        ("ИИ", "AI", "ИИ", "CS601", 4),
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
    
    print("Предметы созданы")
    
    # Создаем преподавателей
    teachers_data = [
        ("Айгуль", "Исакова", "Кожобековна", "a.isakova@college.kg", "Математический", "Профессор"),
        ("Мирлан", "Петров", "Сергеевич", "m.petrov@college.kg", "Физический", "Доцент"),
        ("Нурбек", "Сидоров", "Алымович", "n.sidorov@college.kg", "Информатики", "Старший преподаватель"),
        ("Сара", "Джонс", "Майкловна", "s.jones@college.kg", "Иностранных языков", "Преподаватель"),
        ("Лилия", "Ким", "Владимировна", "l.kim@college.kg", "Экономический", "Доцент"),
        ("Данияр", "Нурматов", "Курманович", "d.nurmatov@college.kg", "Информатики", "Преподаватель"),
        ("Мирбек", "Смирнов", "Канатович", "m.smirnov@college.kg", "Информатики", "Профессор"),
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
    
    print("Преподаватели созданы")
    
    # Создаем аудитории
    rooms_data = [
        ("101", "A", 1, 30, "lecture"),
        ("102", "A", 1, 25, "computer"),
        ("201", "A", 2, 35, "lecture"),
        ("202", "A", 2, 20, "computer"),
        ("301", "B", 3, 40, "lecture"),
        ("302", "B", 3, 15, "computer"),
        ("Спортзал", "C", 1, 50, "gym"),
        ("Лаб-1", "B", 2, 20, "lab"),
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
    
    print("Аудитории созданы")
    
    # Создаем расписание
    today = date.today()
    start_date = today - timedelta(days=today.weekday())  # Понедельник текущей недели
    end_date = start_date + timedelta(days=120)  # На 4 месяца вперед
    
    # Получаем созданные объекты
    cs101 = StudyGroup.objects.get(name="CS-101")
    cs102 = StudyGroup.objects.get(name="CS-102")
    bus201 = StudyGroup.objects.get(name="BUS-201")
    
    math_subject = Subject.objects.get(code="MATH101")
    physics_subject = Subject.objects.get(code="PHYS101")
    programming_subject = Subject.objects.get(code="CS101")
    english_subject = Subject.objects.get(code="ENG101")
    
    teacher_math = Teacher.objects.get(email="a.isakova@college.kg")
    teacher_physics = Teacher.objects.get(email="m.petrov@college.kg")
    teacher_programming = Teacher.objects.get(email="n.sidorov@college.kg")
    teacher_english = Teacher.objects.get(email="s.jones@college.kg")
    
    room_101 = Room.objects.get(number="101", building="A")
    room_102 = Room.objects.get(number="102", building="A")
    room_201 = Room.objects.get(number="201", building="A")
    
    slot_1 = TimeSlot.objects.get(number=1)
    slot_2 = TimeSlot.objects.get(number=2)
    slot_3 = TimeSlot.objects.get(number=3)
    
    # Создаем записи расписания
    schedule_data = [
        # Понедельник
        (cs101, math_subject, teacher_math, room_101, slot_1, 1, "lecture"),
        (cs102, physics_subject, teacher_physics, room_201, slot_1, 1, "lecture"),
        (cs101, programming_subject, teacher_programming, room_102, slot_2, 1, "practice"),
        (bus201, english_subject, teacher_english, room_101, slot_3, 1, "seminar"),
        
        # Вторник
        (cs101, physics_subject, teacher_physics, room_201, slot_1, 2, "lecture"),
        (cs102, math_subject, teacher_math, room_101, slot_2, 2, "lecture"),
        (cs101, english_subject, teacher_english, room_101, slot_3, 2, "seminar"),
        
        # Среда
        (cs101, programming_subject, teacher_programming, room_102, slot_1, 3, "lab"),
        (cs102, programming_subject, teacher_programming, room_102, slot_2, 3, "lab"),
        (bus201, math_subject, teacher_math, room_101, slot_3, 3, "lecture"),
    ]
    
    for group, subject, teacher, room, time_slot, weekday, lesson_type in schedule_data:
        Schedule.objects.get_or_create(
            group=group,
            subject=subject,
            teacher=teacher,
            room=room,
            time_slot=time_slot,
            weekday=weekday,
            start_date=start_date,
            end_date=end_date,
            defaults={
                'lesson_type': lesson_type,
                'week_type': 'all',
                'is_active': True,
                'notes': 'Тестовые данные'
            }
        )
    
    print("Расписание создано")
    print("Тестовые данные успешно загружены!")

if __name__ == "__main__":
    create_test_data()