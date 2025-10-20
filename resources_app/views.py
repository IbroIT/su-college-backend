from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import EducationalResource, LibraryFeature, LibraryStat, WorkingHours, ResourceCategory
from .serializers import EducationalResourceSerializer, LibraryFeatureSerializer, LibraryStatSerializer, WorkingHoursSerializer

class EducationalResourceViewSet(viewsets.ModelViewSet):
    queryset = EducationalResource.objects.filter(is_available=True)
    serializer_class = EducationalResourceSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить ресурсы с переводами"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        resources = EducationalResource.objects.filter(is_available=True).select_related('category').order_by('order')
        
        data = []
        for resource in resources:
            resource_data = {
                'id': resource.id,
                'title': getattr(resource, f'title_{language}', resource.title_ru),
                'description': getattr(resource, f'description_{language}', resource.description_ru),
                'count': resource.count,
                'available_count': resource.available_count,
                'resource_type': resource.resource_type,
                'access_type': resource.access_type,
                'access_url': resource.access_url,
                'download_url': resource.download_url,
                'is_featured': resource.is_featured,
                'views': resource.views,
                'category': {
                    'name': getattr(resource.category, f'name_{language}', resource.category.name_ru),
                    'icon': resource.category.icon,
                    'color': resource.category.color,
                    'bg_color': resource.category.bg_color,
                    'border_color': resource.category.border_color
                }
            }
            data.append(resource_data)
        
        return Response(data)

class LibraryFeatureViewSet(viewsets.ModelViewSet):
    queryset = LibraryFeature.objects.all()
    serializer_class = LibraryFeatureSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить функции библиотеки с переводами"""
        language = get_language()
        features = LibraryFeature.objects.all().order_by('order')
        
        data = []
        for feature in features:
            data.append({
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color
            })
        
        return Response(data)

class LibraryStatViewSet(viewsets.ModelViewSet):
    queryset = LibraryStat.objects.all()
    serializer_class = LibraryStatSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить статистику с переводами"""
        language = get_language()
        stats = LibraryStat.objects.all().order_by('order')
        
        data = []
        for stat in stats:
            data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response(data)

class WorkingHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить часы работы с переводами"""
        language = get_language()
        hours = WorkingHours.objects.all().order_by('order')
        
        data = []
        for hour in hours:
            data.append({
                'day': getattr(hour, f'day_{language}', hour.day_ru),
                'time': getattr(hour, f'time_{language}', hour.time_ru)
            })
        
        return Response(data)

class ResourcesDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        """Получить все данные ресурсов"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        # Ресурсы
        resources = EducationalResource.objects.filter(is_available=True).select_related('category').order_by('order')
        resources_data = []
        for resource in resources:
            resource_info = {
                'id': resource.id,
                'title': getattr(resource, f'title_{language}', resource.title_ru),
                'description': getattr(resource, f'description_{language}', resource.description_ru),
                'count': resource.count,
                'resource_type': resource.resource_type,
                'access_type': resource.access_type,
                'access_url': resource.access_url,
                'download_url': resource.download_url,
                'category': {
                    'name': getattr(resource.category, f'name_{language}', resource.category.name_ru),
                    'icon': resource.category.icon,
                    'color': resource.category.color,
                    'bg_color': resource.category.bg_color,
                    'border_color': resource.category.border_color
                }
            }
            resources_data.append(resource_info)
        
        # Функции библиотеки
        features = LibraryFeature.objects.all().order_by('order')
        features_data = []
        for feature in features:
            features_data.append({
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color
            })
        
        # Статистика
        stats = LibraryStat.objects.all().order_by('order')
        stats_data = []
        for stat in stats:
            stats_data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        # Часы работы
        hours = WorkingHours.objects.all().order_by('order')
        hours_data = []
        for hour in hours:
            hours_data.append({
                'day': getattr(hour, f'day_{language}', hour.day_ru),
                'time': getattr(hour, f'time_{language}', hour.time_ru)
            })
        
        return Response({
            'resources': resources_data,
            'features': features_data,
            'stats': stats_data,
            'hours': hours_data
        })