from rest_framework import serializers
from .models import CouncilFeature, CouncilMember, CouncilEvent, CouncilStat

class CouncilFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilFeature
        fields = ['id', 'icon', 'title_ru', 'title_kg', 'title_en', 
                 'description_ru', 'description_kg', 'description_en', 
                 'color', 'order']

class CouncilMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilMember
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 
                 'position_ru', 'position_kg', 'position_en',
                 'bio_ru', 'bio_kg', 'bio_en', 'image',
                 'position_type', 'instagram', 'email', 'linkedin',
                 'is_active', 'order']

class CouncilEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilEvent
        fields = ['id', 'title_ru', 'title_kg', 'title_en',
                 'description_ru', 'description_kg', 'description_en',
                 'date', 'participants', 'location', 'is_active', 'order']

class CouncilStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncilStat
        fields = ['id', 'number', 'label_ru', 'label_kg', 'label_en', 'order']