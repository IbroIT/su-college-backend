from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)

urlpatterns = [
    path('teachers/', views.TeacherViewSet.as_view({'get': 'list'}), name='teachers-list'),
    path('teachers/with_translations/', views.TeacherViewSet.as_view({'get': 'with_translations'}), name='teachers-with-translations'),
    path('teachers/active/', views.TeacherViewSet.as_view({'get': 'active'}), name='teachers-active'),
    path('teachers/<int:pk>/', views.TeacherViewSet.as_view({'get': 'retrieve'}), name='teachers-detail'),
]