from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, time, timedelta
from .models import StudyGroup, Subject, Teacher, Room, TimeSlot, Schedule


class ScheduleModelTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.group = StudyGroup.objects.create(
            name="CS-101",
            course=1,
            faculty="Computer Science"
        )
        
        self.subject = Subject.objects.create(
            name_ru="Математика",
            name_en="Mathematics",
            name_ky="Математика",
            code="MATH101",
            credits=4
        )
        
        self.teacher = Teacher.objects.create(
            first_name="Иван",
            last_name="Иванов",
            email="ivanov@example.com",
            department="Математический",
            position="Профессор"
        )
        
        self.room = Room.objects.create(
            number="101",
            building="A",
            floor=1,
            capacity=30,
            room_type="lecture"
        )
        
        self.time_slot = TimeSlot.objects.create(
            number=1,
            start_time=time(8, 30),
            end_time=time(10, 0)
        )
    
    def test_schedule_creation(self):
        """Тест создания расписания"""
        schedule = Schedule.objects.create(
            group=self.group,
            subject=self.subject,
            teacher=self.teacher,
            room=self.room,
            time_slot=self.time_slot,
            weekday=1,
            lesson_type="lecture",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90)
        )
        
        self.assertEqual(schedule.group, self.group)
        self.assertEqual(schedule.subject, self.subject)
        self.assertTrue(schedule.is_active)
    
    def test_schedule_validation_date_order(self):
        """Тест валидации порядка дат"""
        with self.assertRaises(ValidationError):
            schedule = Schedule(
                group=self.group,
                subject=self.subject,
                teacher=self.teacher,
                room=self.room,
                time_slot=self.time_slot,
                weekday=1,
                lesson_type="lecture",
                start_date=date.today() + timedelta(days=90),
                end_date=date.today()
            )
            schedule.full_clean()
    
    def test_teacher_conflict(self):
        """Тест конфликта преподавателя"""
        # Создаем первое расписание
        Schedule.objects.create(
            group=self.group,
            subject=self.subject,
            teacher=self.teacher,
            room=self.room,
            time_slot=self.time_slot,
            weekday=1,
            lesson_type="lecture",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90)
        )
        
        # Создаем вторую группу
        group2 = StudyGroup.objects.create(
            name="CS-102",
            course=1,
            faculty="Computer Science"
        )
        
        # Создаем вторую аудиторию
        room2 = Room.objects.create(
            number="102",
            building="A",
            floor=1,
            capacity=30,
            room_type="lecture"
        )
        
        # Пытаемся создать конфликтующее расписание
        with self.assertRaises(ValidationError):
            schedule2 = Schedule(
                group=group2,
                subject=self.subject,
                teacher=self.teacher,  # Тот же преподаватель
                room=room2,
                time_slot=self.time_slot,  # То же время
                weekday=1,  # Тот же день
                lesson_type="lecture",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=90)
            )
            schedule2.full_clean()
    
    def test_subject_multilingual(self):
        """Тест многоязычности предметов"""
        self.assertEqual(self.subject.name_ru, "Математика")
        self.assertEqual(self.subject.name_en, "Mathematics")
        self.assertEqual(self.subject.name_ky, "Математика")
    
    def test_teacher_str_representation(self):
        """Тест строкового представления преподавателя"""
        expected = "Иванов И."
        self.assertEqual(str(self.teacher), expected)
    
    def test_room_str_representation(self):
        """Тест строкового представления аудитории"""
        expected = "A-101"
        self.assertEqual(str(self.room), expected)