# tests/serializers.py

from rest_framework import serializers
from .models import Test, MatchingQuestion, FillInTheBlanksQuestion, MCQQuestion

class MatchingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingQuestion
        fields = ['id', 'question', 'correct_answer']

class FillInTheBlanksQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillInTheBlanksQuestion
        fields = ['id', 'question', 'correct_answer', 'options']

class MCQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQQuestion
        fields = ['id', 'question', 'correct_answer', 'choices']

class TestSerializer(serializers.ModelSerializer):
    matching_questions = MatchingQuestionSerializer(many=True, read_only=True)
    fill_in_the_blanks_questions = FillInTheBlanksQuestionSerializer(many=True, read_only=True)
    mcq_questions = MCQQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'matching_questions', 'fill_in_the_blanks_questions', 'mcq_questions']
