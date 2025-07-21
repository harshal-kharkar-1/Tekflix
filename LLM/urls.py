from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('api/process/<int:pk>/', views.process_project, name='process_project'),
    path('api/status/<int:pk>/', views.project_status, name='project_status'),
    path('export/<int:pk>/', views.export_project, name='export_project'),
]