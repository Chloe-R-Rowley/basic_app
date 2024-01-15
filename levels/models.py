# levels/models.py

from django.db import models

class Level(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    lesson_number = models.PositiveIntegerField()
    lesson_name = models.CharField(max_length=255)
    french_phrase = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)

    def __str__(self):
        return f"Lesson {self.lesson_number} - {self.lesson_name} ({self.level})"