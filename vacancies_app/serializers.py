from rest_framework import serializers
from .models import VacancyCategory, Vacancy, Benefit, VacancyStat, ApplicationInfo

class VacancyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyCategory
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'icon', 'color', 'bg_color', 'order']

class VacancySerializer(serializers.ModelSerializer):
    category = VacancyCategorySerializer(read_only=True)
    
    class Meta:
        model = Vacancy
        fields = ['id', 'title_ru', 'title_kg', 'title_en', 'description_ru', 'description_kg', 'description_en',
                 'category', 'requirements_ru', 'requirements_kg', 'requirements_en', 'salary', 'work_schedule',
                 'employment_type', 'contact_email', 'contact_person', 'contact_phone', 'status', 'is_featured',
                 'is_urgent', 'order', 'deadline', 'created_at']

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ['id', 'icon', 'title_ru', 'title_kg', 'title_en', 
                 'description_ru', 'description_kg', 'description_en', 'order']

class VacancyStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyStat
        fields = ['number', 'label_ru', 'label_kg', 'label_en', 'order']

class ApplicationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationInfo
        fields = ['email', 'subject_template_ru', 'subject_template_kg', 'subject_template_en',
                 'deadline_text_ru', 'deadline_text_kg', 'deadline_text_en',
                 'documents_ru', 'documents_kg', 'documents_en']