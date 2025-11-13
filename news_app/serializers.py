from rest_framework import serializers
from .models import News, Category, NewsImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'slug', 'color']

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'caption_ru', 'caption_kg', 'caption_en', 'order']

class NewsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title_ru', 'title_kg', 'title_en',
            'excerpt_ru', 'excerpt_kg', 'excerpt_en',
            'image', 'date', 'category', 'is_featured',
            'pinned',
            'slug', 'views'
        ]

class NewsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = NewsImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title_ru', 'title_kg', 'title_en',
            'excerpt_ru', 'excerpt_kg', 'excerpt_en',
            'content_ru', 'content_kg', 'content_en',
            'image', 'date', 'category', 'is_featured',
            'pinned',
            'slug', 'views', 'images', 'created_at'
        ]