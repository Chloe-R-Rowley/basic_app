# language_learning/urls.py

from django.urls import path, include

urlpatterns = [
    path('api/users/', include('users.urls')),
    path('api/levels/', include('levels.urls')),
    path('api/progress/', include('progress.urls')),
]
