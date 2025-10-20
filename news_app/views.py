from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from django.db.models import Q
from .models import News, Category
from .serializers import NewsListSerializer, NewsDetailSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsListSerializer
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsDetailSerializer
        return NewsListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные новости"""
        featured_news = self.queryset.filter(is_featured=True).order_by('-date')[:6]
        serializer = self.get_serializer(featured_news, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить новости с переводами для текущего языка"""
        language = get_language()
        
        # Получаем язык из параметра, если передан
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        news = self.queryset.order_by('-date')
        data = []
        
        for item in news:
            news_data = {
                'id': item.id,
                'title': getattr(item, f'title_{language}', item.title_ru),
                'excerpt': getattr(item, f'excerpt_{language}', item.excerpt_ru),
                'content': getattr(item, f'content_{language}', item.content_ru),
                'image': request.build_absolute_uri(item.image.url) if item.image else None,
                'date': item.date,
                'is_featured': item.is_featured,
                'slug': item.slug,
                'views': item.views,
                'category': {
                    'id': item.category.id,
                    'name': getattr(item.category, f'name_{language}', item.category.name_ru),
                    'color': item.category.color,
                    'slug': item.category.slug
                }
            }
            data.append(news_data)
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Поиск новостей"""
        query = request.GET.get('q', '')
        language = get_language()
        
        if query:
            # Поиск по всем языковым полям
            news = self.queryset.filter(
                Q(title_ru__icontains=query) |
                Q(title_kg__icontains=query) |
                Q(title_en__icontains=query) |
                Q(excerpt_ru__icontains=query) |
                Q(excerpt_kg__icontains=query) |
                Q(excerpt_en__icontains=query)
            ).order_by('-date')
        else:
            news = self.queryset.order_by('-date')
        
        data = []
        for item in news:
            news_data = {
                'id': item.id,
                'title': getattr(item, f'title_{language}', item.title_ru),
                'excerpt': getattr(item, f'excerpt_{language}', item.excerpt_ru),
                'image': request.build_absolute_uri(item.image.url) if item.image else None,
                'date': item.date,
                'slug': item.slug,
                'category': {
                    'name': getattr(item.category, f'name_{language}', item.category.name_ru),
                    'color': item.category.color
                }
            }
            data.append(news_data)
        
        return Response(data)