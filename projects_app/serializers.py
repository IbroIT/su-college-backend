from rest_framework import serializers
from .models import StudentProject, ProjectFeature, ProjectTechnology, ProjectStat

class ProjectFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFeature
        fields = ['text_ru', 'text_kg', 'text_en', 'order']

class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = ['name', 'icon', 'color', 'order']

class StudentProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProject
        fields = ['id', 'student_name_ru', 'student_name_kg', 'student_name_en',
                 'title_ru', 'title_kg', 'title_en', 'student_image',
                 'github_url', 'website_url', 'is_featured', 'order']

class StudentProjectDetailSerializer(serializers.ModelSerializer):
    features = ProjectFeatureSerializer(many=True, read_only=True)
    technologies = ProjectTechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = StudentProject
        fields = ['id', 'student_name_ru', 'student_name_kg', 'student_name_en',
                 'title_ru', 'title_kg', 'title_en', 'description_ru', 'description_kg', 'description_en',
                 'student_image', 'project_image', 'github_url', 'website_url', 'demo_url',
                 'is_featured', 'views', 'created_at', 'features', 'technologies']

class ProjectStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStat
        fields = ['number', 'label_ru', 'label_kg', 'label_en', 'order']