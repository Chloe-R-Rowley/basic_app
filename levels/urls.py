# levels/urls.py

from django.urls import path
from .views import LessonDetailView, LessonListCreateView, LevelListView

urlpatterns = [
    path('levels/', LevelListView.as_view(), name='level-list'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
