from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import CouncilFeature, CouncilMember, CouncilEvent, CouncilStat
from .serializers import CouncilFeatureSerializer, CouncilMemberSerializer, CouncilEventSerializer, CouncilStatSerializer

class CouncilFeatureViewSet(viewsets.ModelViewSet):
    queryset = CouncilFeature.objects.all()
    serializer_class = CouncilFeatureSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        language = get_language()
        features = CouncilFeature.objects.all().order_by('order')
        
        data = []
        for feature in features:
            data.append({
                'id': feature.id,
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color,
                'order': feature.order
            })
        
        return Response(data)

class CouncilMemberViewSet(viewsets.ModelViewSet):
    queryset = CouncilMember.objects.filter(is_active=True)
    serializer_class = CouncilMemberSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        language = get_language()
        members = CouncilMember.objects.filter(is_active=True).order_by('order')
        
        data = []
        for member in members:
            data.append({
                'id': member.id,
                'name': getattr(member, f'name_{language}', member.name_ru),
                'position': getattr(member, f'position_{language}', member.position_ru),
                'bio': getattr(member, f'bio_{language}', member.bio_ru),
                'image': request.build_absolute_uri(member.image.url) if member.image else None,
                'position_type': member.position_type,
                'instagram': member.instagram,
                'email': member.email,
                'linkedin': member.linkedin,
                'order': member.order
            })
        
        return Response(data)

class CouncilEventViewSet(viewsets.ModelViewSet):
    queryset = CouncilEvent.objects.filter(is_active=True)
    serializer_class = CouncilEventSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        language = get_language()
        from django.utils import timezone
        events = CouncilEvent.objects.filter(is_active=True, date__gte=timezone.now()).order_by('date')[:3]
        
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'title': getattr(event, f'title_{language}', event.title_ru),
                'description': getattr(event, f'description_{language}', event.description_ru),
                'date': event.date,
                'participants': event.participants,
                'location': event.location,
                'order': event.order
            })
        
        return Response(data)

class CouncilStatViewSet(viewsets.ModelViewSet):
    queryset = CouncilStat.objects.all()
    serializer_class = CouncilStatSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        language = get_language()
        stats = CouncilStat.objects.all().order_by('order')
        
        data = []
        for stat in stats:
            data.append({
                'id': stat.id,
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru),
                'order': stat.order
            })
        
        return Response(data)

class CouncilDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        """Получить все данные совета с переводами"""
        language = get_language()
        
        # Получаем язык из параметра, если передан
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        # Функции совета
        features = CouncilFeature.objects.all().order_by('order')
        features_data = []
        for feature in features:
            features_data.append({
                'icon': feature.icon,
                'title': getattr(feature, f'title_{language}', feature.title_ru),
                'description': getattr(feature, f'description_{language}', feature.description_ru),
                'color': feature.color
            })
        
        # Члены совета
        members = CouncilMember.objects.filter(is_active=True).order_by('order')
        members_data = []
        for member in members:
            members_data.append({
                'name': getattr(member, f'name_{language}', member.name_ru),
                'position': getattr(member, f'position_{language}', member.position_ru),
                'bio': getattr(member, f'bio_{language}', member.bio_ru),
                'image': request.build_absolute_uri(member.image.url) if member.image else None,
                'instagram': member.instagram,
                'email': member.email,
                'linkedin': member.linkedin
            })
        
        # Мероприятия
        from django.utils import timezone
        events = CouncilEvent.objects.filter(is_active=True, date__gte=timezone.now()).order_by('date')[:3]
        events_data = []
        for event in events:
            events_data.append({
                'title': getattr(event, f'title_{language}', event.title_ru),
                'description': getattr(event, f'description_{language}', event.description_ru),
                'date': event.date,
                'participants': event.participants
            })
        
        # Статистика
        stats = CouncilStat.objects.all().order_by('order')
        stats_data = []
        for stat in stats:
            stats_data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response({
            'features': features_data,
            'members': members_data,
            'events': events_data,
            'stats': stats_data
        })