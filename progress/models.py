# progress/models.py

from django.db import models
from django.contrib.auth.models import User
from levels.models import Level, Lesson

class Badge(models.Model):
    name = models.CharField(max_length=255)
    # Add other fields for the badge

    def __str__(self):
        return self.name

class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    
    lessons_completed = models.ManyToManyField(Lesson, related_name='completed_lessons', blank=True)
    tests_answered = models.PositiveIntegerField(default=0)
    test_scores = models.PositiveIntegerField(default=0)
    coins_received = models.PositiveIntegerField(default=0)
    badges_received = models.ManyToManyField(Badge, related_name='received_badges', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Progress"
