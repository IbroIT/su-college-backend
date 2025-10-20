from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import Teacher
from .serializers import TeacherSerializer, TeacherListSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherSerializer

    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить преподавателей с переводами для текущего языка"""
        # Сопоставление кода языка и поля в модели
        LANG_MAP = {
            'ky': 'kg',  # Если фронтенд отправляет 'ky', а в модели поле 'name_kg'
            'ru': 'ru',
            'en': 'en',
        }

        language = get_language()  # Получаем язык текущей сессии
        lang_code = LANG_MAP.get(language, 'ru')  # fallback на русский

        teachers = Teacher.objects.filter(is_active=True).prefetch_related('achievements').order_by('order')
        data = []

        for teacher in teachers:
            teacher_data = {
                'id': teacher.id,
                'name': getattr(teacher, f'name_{lang_code}', teacher.name_ru),
                'subject': getattr(teacher, f'subject_{lang_code}', teacher.subject_ru),
                'image': request.build_absolute_uri(teacher.image.url) if teacher.image else None,
                'experience': getattr(teacher, f'experience_{lang_code}', teacher.experience_ru),
                'description': getattr(teacher, f'description_{lang_code}', teacher.description_ru),
                'rating': teacher.rating,
                'color': teacher.color,
                'achievements': []
            }

            for achievement in teacher.achievements.all().order_by('order'):
                teacher_data['achievements'].append(
                    getattr(achievement, f'text_{lang_code}', achievement.text_ru)
                )

            data.append(teacher_data)

    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить преподавателей с переводами для указанного языка"""
        print("=== HEADERS ===")
        for key, value in request.META.items():
            if 'HTTP' in key:
                print(f"{key}: {value}")

        # Получаем язык из параметра URL
        lang = request.GET.get('lang', 'ru').lower()
        print(f"Requested language from param: {lang}")

        # Поддерживаемые языки
        supported_languages = ['ru', 'kg', 'en']
        if lang not in supported_languages:
            lang = 'ru'

        print(f"Final language: {lang}")

        teachers = Teacher.objects.filter(is_active=True).prefetch_related('achievements').order_by('order')
        data = []

        for teacher in teachers:
            # Получаем данные для выбранного языка
            name = getattr(teacher, f'name_{lang}', teacher.name_ru)
            subject = getattr(teacher, f'subject_{lang}', teacher.subject_ru)
            experience = getattr(teacher, f'experience_{lang}', teacher.experience_ru)
            description = getattr(teacher, f'description_{lang}', teacher.description_ru)

            print(f"Teacher: {teacher.name_ru} -> {lang}: {name}")

            teacher_data = {
                'id': teacher.id,
                'name': name,
                'subject': subject,
                'image': request.build_absolute_uri(teacher.image.url) if teacher.image else None,
                'experience': experience,
                'description': description,
                'rating': teacher.rating,
                'color': teacher.color,
                'achievements': []
            }

            # Обрабатываем достижения
            for achievement in teacher.achievements.all().order_by('order'):
                achievement_text = getattr(achievement, f'text_{lang}', achievement.text_ru)
                teacher_data['achievements'].append(achievement_text)

            data.append(teacher_data)

        print(f"Returning data for {len(data)} teachers in language: {lang}")
        return Response(data)