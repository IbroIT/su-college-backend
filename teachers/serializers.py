from rest_framework import serializers
from .models import Teacher, Achievement

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['text_ru', 'text_kg', 'text_en', 'order']

class TeacherSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'name_ru', 'name_kg', 'name_en',
            'subject_ru', 'subject_kg', 'subject_en',
            'image', 'experience_ru', 'experience_kg', 'experience_en',
            'description_ru', 'description_kg', 'description_en',
            'rating', 'color', 'achievements',
            'is_active', 'order'
        ]

class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id', 'name_ru', 'name_kg', 'name_en', 
            'subject_ru', 'subject_kg', 'subject_en', 
            'image', 'is_active'
        ]