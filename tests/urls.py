# tests/urls.py

from django.urls import path
from .views import CheckAndReward, GetFillInTheBlanksQuestions, GetMCQQuestions, GetMatchingQuestions, TestListView
from .views import TestListView

urlpatterns = [
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:test_id>/matching-questions/', GetMatchingQuestions.as_view(), name='get-matching-questions'),
    path('tests/<int:test_id>/fill-in-the-blanks-questions/', GetFillInTheBlanksQuestions.as_view(), name='get-fill-in-the-blanks-questions'),
    path('tests/<int:test_id>/mcq-questions/', GetMCQQuestions.as_view(), name='get-mcq-questions'),
    path('tests/<int:test_id>/check-and-reward/', CheckAndReward.as_view(), name='check-and-reward'),
]
