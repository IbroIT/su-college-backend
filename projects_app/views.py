from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import StudentProject, ProjectStat
from .serializers import StudentProjectDetailSerializer, ProjectStatSerializer

class StudentProjectViewSet(viewsets.ModelViewSet):
    queryset = StudentProject.objects.filter(is_published=True)
    serializer_class = StudentProjectDetailSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить проекты с переводами"""
        language = get_language()
        
        # Получаем язык из параметра, если передан
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        projects = StudentProject.objects.filter(is_published=True).prefetch_related('features', 'technologies').order_by('order')
        
        data = []
        for project in projects:
            project_data = {
                'id': project.id,
                'name': getattr(project, f'student_name_{language}', project.student_name_ru),
                'title': getattr(project, f'title_{language}', project.title_ru),
                'description': getattr(project, f'description_{language}', project.description_ru),
                'image': request.build_absolute_uri(project.student_image.url) if project.student_image else None,
                'project_image': request.build_absolute_uri(project.project_image.url) if project.project_image else None,
                'github': project.github_url,
                'website': project.website_url,
                'demo': project.demo_url,
                'is_featured': project.is_featured,
                'views': project.views,
                'technologies': [],
                'features': []
            }
            
            # Технологии
            for tech in project.technologies.all().order_by('order'):
                project_data['technologies'].append({
                    'name': tech.name,
                    'icon': tech.icon,
                    'color': tech.color
                })
            
            # Особенности
            for feature in project.features.all().order_by('order'):
                feature_text = getattr(feature, f'text_{language}', feature.text_ru)
                project_data['features'].append(feature_text)
            
            data.append(project_data)
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные проекты"""
        language = get_language()
        featured_projects = StudentProject.objects.filter(is_published=True, is_featured=True).order_by('order')
        
        data = []
        for project in featured_projects:
            project_data = {
                'id': project.id,
                'name': getattr(project, f'student_name_{language}', project.student_name_ru),
                'title': getattr(project, f'title_{language}', project.title_ru),
                'image': request.build_absolute_uri(project.student_image.url) if project.student_image else None,
                'github': project.github_url,
                'website': project.website_url,
            }
            data.append(project_data)
        
        return Response(data)

class ProjectStatViewSet(viewsets.ModelViewSet):
    queryset = ProjectStat.objects.all()
    serializer_class = ProjectStatSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить статистику с переводами"""
        language = get_language()
        stats = ProjectStat.objects.all().order_by('order')
        
        data = []
        for stat in stats:
            data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response(data)

class ProjectsDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        """Получить все данные проектов"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        # Проекты
        projects = StudentProject.objects.filter(is_published=True).prefetch_related('features', 'technologies').order_by('order')
        projects_data = []
        for project in projects:
            project_info = {
                'name': getattr(project, f'student_name_{language}', project.student_name_ru),
                'title': getattr(project, f'title_{language}', project.title_ru),
                'description': getattr(project, f'description_{language}', project.description_ru),
                'image': request.build_absolute_uri(project.student_image.url) if project.student_image else None,
                'project_image': request.build_absolute_uri(project.project_image.url) if project.project_image else None,
                'github': project.github_url,
                'website': project.website_url,
                'demo': project.demo_url,
                'technologies': [],
                'features': []
            }
            
            for tech in project.technologies.all().order_by('order'):
                project_info['technologies'].append(tech.name)
            
            for feature in project.features.all().order_by('order'):
                feature_text = getattr(feature, f'text_{language}', feature.text_ru)
                project_info['features'].append(feature_text)
            
            projects_data.append(project_info)
        
        # Статистика
        stats = ProjectStat.objects.all().order_by('order')
        stats_data = []
        for stat in stats:
            stats_data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response({
            'projects': projects_data,
            'stats': stats_data
        })