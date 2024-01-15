# tests/models.py

from django.db import models
from levels.models import Level
from django.contrib.auth.models import User

class Test(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class MatchingQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

class FillInTheBlanksQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    options = models.JSONField()  # Store options as a JSON array

    def __str__(self):
        return self.question

class MCQQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    choices = models.JSONField()  # Store choices as a JSON array

    def __str__(self):
        return self.question

class UserAnswer(models.Model):
    QUESTION_TYPES = (
        ('matching', 'Matching'),
        ('fill_in_the_blanks', 'Fill in the Blanks'),
        ('mcq', 'Multiple Choice Questions'),
    )

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.PositiveIntegerField()
    user_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s answer for {self.question_type} question {self.question_id}"
