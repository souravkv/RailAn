"""
URL configuration for announcements app
"""
from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('list/', views.announcement_list, name='announcement_list'),
    path('announcement/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('display/', views.display_board, name='display_board'),
    path('display/<int:board_id>/', views.display_board, name='display_board'),
    
    # API endpoints
    path('api/announcement/<int:announcement_id>/status/', views.api_announcement_status, name='api_announcement_status'),
    path('api/announcement/create/', views.api_create_announcement, name='api_create_announcement'),
]

