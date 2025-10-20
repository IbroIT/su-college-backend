from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import Vacancy, Benefit, VacancyStat, ApplicationInfo, VacancyCategory
from .serializers import VacancySerializer, BenefitSerializer, VacancyStatSerializer, ApplicationInfoSerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.filter(status='active')
    serializer_class = VacancySerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить вакансии с переводами"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        vacancies = Vacancy.objects.filter(status='active').select_related('category').order_by('order')
        
        data = []
        for vacancy in vacancies:
            vacancy_data = {
                'id': vacancy.id,
                'title': getattr(vacancy, f'title_{language}', vacancy.title_ru),
                'description': getattr(vacancy, f'description_{language}', vacancy.description_ru),
                'requirements': getattr(vacancy, f'requirements_{language}', vacancy.requirements_ru),
                'salary': vacancy.salary,
                'work_schedule': vacancy.work_schedule,
                'employment_type': vacancy.employment_type,
                'contact_email': vacancy.contact_email,
                'contact_person': vacancy.contact_person,
                'contact_phone': vacancy.contact_phone,
                'is_featured': vacancy.is_featured,
                'is_urgent': vacancy.is_urgent,
                'deadline': vacancy.deadline,
                'category': {
                    'name': getattr(vacancy.category, f'name_{language}', vacancy.category.name_ru),
                    'icon': vacancy.category.icon,
                    'color': vacancy.category.color,
                    'bg_color': vacancy.category.bg_color
                }
            }
            data.append(vacancy_data)
        
        return Response(data)

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить преимущества с переводами"""
        language = get_language()
        benefits = Benefit.objects.all().order_by('order')
        
        data = []
        for benefit in benefits:
            data.append({
                'icon': benefit.icon,
                'title': getattr(benefit, f'title_{language}', benefit.title_ru),
                'description': getattr(benefit, f'description_{language}', benefit.description_ru)
            })
        
        return Response(data)

class VacancyStatViewSet(viewsets.ModelViewSet):
    queryset = VacancyStat.objects.all()
    serializer_class = VacancyStatSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить статистику с переводами"""
        language = get_language()
        stats = VacancyStat.objects.all().order_by('order')
        
        data = []
        for stat in stats:
            data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        return Response(data)

class ApplicationInfoViewSet(viewsets.ModelViewSet):
    queryset = ApplicationInfo.objects.all()
    serializer_class = ApplicationInfoSerializer
    
    @action(detail=False, methods=['get'])
    def with_translations(self, request):
        """Получить информацию о заявках с переводами"""
        language = get_language()
        try:
            app_info = ApplicationInfo.objects.first()
            if app_info:
                data = {
                    'email': app_info.email,
                    'subject': getattr(app_info, f'subject_template_{language}', app_info.subject_template_ru),
                    'deadline': getattr(app_info, f'deadline_text_{language}', app_info.deadline_text_ru),
                    'documents': getattr(app_info, f'documents_{language}', app_info.documents_ru)
                }
            else:
                data = {
                    'email': 'hr-smu@list.ru',
                    'subject': 'Заявка на вакансию',
                    'deadline': 'Принимаются постоянно',
                    'documents': ['Резюме', 'Сопроводительное письмо']
                }
        except:
            data = {
                'email': 'hr-smu@list.ru',
                'subject': 'Заявка на вакансию',
                'deadline': 'Принимаются постоянно',
                'documents': ['Резюме', 'Сопроводительное письмо']
            }
        
        return Response(data)

class VacanciesDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def all_data(self, request):
        """Получить все данные вакансий"""
        language = get_language()
        
        lang_param = request.GET.get('lang')
        if lang_param in ['ru', 'kg', 'en']:
            language = lang_param
        
        # Вакансии
        vacancies = Vacancy.objects.filter(status='active').select_related('category').order_by('order')
        vacancies_data = []
        for vacancy in vacancies:
            vacancy_info = {
                'id': vacancy.id,
                'title': getattr(vacancy, f'title_{language}', vacancy.title_ru),
                'description': getattr(vacancy, f'description_{language}', vacancy.description_ru),
                'requirements': getattr(vacancy, f'requirements_{language}', vacancy.requirements_ru),
                'salary': vacancy.salary,
                'work_schedule': vacancy.work_schedule,
                'employment_type': vacancy.employment_type,
                'contact_email': vacancy.contact_email,
                'is_featured': vacancy.is_featured,
                'is_urgent': vacancy.is_urgent,
                'deadline': vacancy.deadline,
                'category': {
                    'name': getattr(vacancy.category, f'name_{language}', vacancy.category.name_ru),
                    'icon': vacancy.category.icon,
                    'color': vacancy.category.color,
                    'bg_color': vacancy.category.bg_color
                }
            }
            vacancies_data.append(vacancy_info)
        
        # Преимущества
        benefits = Benefit.objects.all().order_by('order')
        benefits_data = []
        for benefit in benefits:
            benefits_data.append({
                'icon': benefit.icon,
                'title': getattr(benefit, f'title_{language}', benefit.title_ru),
                'description': getattr(benefit, f'description_{language}', benefit.description_ru)
            })
        
        # Статистика
        stats = VacancyStat.objects.all().order_by('order')
        stats_data = []
        for stat in stats:
            stats_data.append({
                'number': stat.number,
                'label': getattr(stat, f'label_{language}', stat.label_ru)
            })
        
        # Информация о заявках
        try:
            app_info = ApplicationInfo.objects.first()
            if app_info:
                application_info = {
                    'email': app_info.email,
                    'subject': getattr(app_info, f'subject_template_{language}', app_info.subject_template_ru),
                    'deadline': getattr(app_info, f'deadline_text_{language}', app_info.deadline_text_ru),
                    'documents': getattr(app_info, f'documents_{language}', app_info.documents_ru)
                }
            else:
                application_info = {
                    'email': 'hr-smu@list.ru',
                    'subject': 'Заявка на вакансию',
                    'deadline': 'Принимаются постоянно',
                    'documents': ['Резюме', 'Сопроводительное письмо']
                }
        except:
            application_info = {
                'email': 'hr-smu@list.ru',
                'subject': 'Заявка на вакансию',
                'deadline': 'Принимаются постоянно',
                'documents': ['Резюме', 'Сопроводительное письмо']
            }
        
        return Response({
            'vacancies': vacancies_data,
            'benefits': benefits_data,
            'stats': stats_data,
            'applicationInfo': application_info
        })