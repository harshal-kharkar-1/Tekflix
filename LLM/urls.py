# # from django.urls import path

# # from . import views

# # urlpatterns = [
# #     path("", views.index, name="index"),
# # ]

# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path("ask/", views.ask_question, name="ask_question"),
# #     # You can add more routes here
# # ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.project_list, name='project_list'),
#     path('create/', views.create_project, name='create_project'),
#     # path('project/<int:project_id>/', views.project_detail, name='project_detail'),
#     path('project/<int:pk>/', views.project_detail, name='project_detail'),

#     path('api/process/<int:project_id>/', views.process_project, name='process_project'),
#     path('api/status/<int:project_id>/', views.project_status, name='project_status'),
#     path('export/<int:project_id>/', views.export_project, name='export_project'),
# ]

from django.urls import path
from . import views
from .views import youtube_to_pdf_view


urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('api/process/<int:pk>/', views.process_project, name='process_project'),
    path('api/status/<int:pk>/', views.project_status, name='project_status'),
    path('export/<int:pk>/', views.export_project, name='export_project'),
    path('youtube-to-pdf/', views.youtube_to_pdf_view, name='youtube_to_pdf'),

]
