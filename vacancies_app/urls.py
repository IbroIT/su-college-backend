from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vacancies', views.VacancyViewSet)
router.register(r'benefits', views.BenefitViewSet)
router.register(r'stats', views.VacancyStatViewSet)
router.register(r'application-info', views.ApplicationInfoViewSet)
router.register(r'data', views.VacanciesDataViewSet, basename='vacancies-data')

urlpatterns = [
    path('', include(router.urls)),
]