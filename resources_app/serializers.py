from rest_framework import serializers
from .models import ResourceCategory, EducationalResource, LibraryFeature, LibraryStat, WorkingHours

class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'icon', 'color', 
                 'bg_color', 'border_color', 'order']

class EducationalResourceSerializer(serializers.ModelSerializer):
    category = ResourceCategorySerializer(read_only=True)
    
    class Meta:
        model = EducationalResource
        fields = ['id', 'title_ru', 'title_kg', 'title_en', 'description_ru', 
                 'description_kg', 'description_en', 'category', 'resource_type',
                 'access_type', 'count', 'available_count', 'access_url',
                 'download_url', 'is_featured', 'is_available', 'order', 'views']

class LibraryFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryFeature
        fields = ['id', 'icon', 'title_ru', 'title_kg', 'title_en', 
                 'description_ru', 'description_kg', 'description_en', 
                 'color', 'order']

class LibraryStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryStat
        fields = ['number', 'label_ru', 'label_kg', 'label_en', 'order']

class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = ['day_ru', 'day_kg', 'day_en', 'time_ru', 'time_kg', 'time_en', 'order']