# levels/serializers.py

from rest_framework import serializers
from .models import Level, Lesson

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'number', 'title', 'description']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'level', 'lesson_number', 'lesson_name', 'french_phrase', 'translation']