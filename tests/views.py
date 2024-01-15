# tests/views.py

from rest_framework import generics
from .models import Test, UserAnswer
from .serializers import TestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test, MatchingQuestion, FillInTheBlanksQuestion, MCQQuestion
from .serializers import TestSerializer, MatchingQuestionSerializer, FillInTheBlanksQuestionSerializer, MCQQuestionSerializer

class TestListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class GetMatchingQuestions(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        matching_questions = MatchingQuestion.objects.filter(test=test)
        serializer = MatchingQuestionSerializer(matching_questions, many=True)
        return Response(serializer.data)

class GetFillInTheBlanksQuestions(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        fill_in_the_blanks_questions = FillInTheBlanksQuestion.objects.filter(test=test)
        serializer = FillInTheBlanksQuestionSerializer(fill_in_the_blanks_questions, many=True)
        return Response(serializer.data)

class GetMCQQuestions(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        mcq_questions = MCQQuestion.objects.filter(test=test)
        serializer = MCQQuestionSerializer(mcq_questions, many=True)
        return Response(serializer.data)
    
class CheckAndReward(APIView):
    def post(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        user_answers = self.request.data.get('user_answers', {})

        # Compare user_answers with correct_answers and award points
        total_correct_answers = self.compare_and_reward(user_answers, test)

        # Update user's coins based on the number of correct answers
        coins_received = total_correct_answers

        return Response({"total_correct_answers": total_correct_answers, "coins_received": coins_received})

    def compare_and_reward(self, user_answers, test):
        total_correct_answers = 0

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # Iterate through user_answers and compare with correct_answers
            for question_type, answers in user_answers.items():
                for question_id, user_answer in answers.items():
                    try:
                        if question_type == 'matching':
                            # Logic to compare matching questions
                            question = MatchingQuestion.objects.get(pk=question_id, test=test)
                            correct_answer = question.correct_answer
                        elif question_type == 'fill_in_the_blanks':
                            # Logic to compare fill-in-the-blanks questions
                            question = FillInTheBlanksQuestion.objects.get(pk=question_id, test=test)
                            correct_answer = question.correct_answer
                        elif question_type == 'mcq':
                            # Logic to compare MCQ questions
                            question = MCQQuestion.objects.get(pk=question_id, test=test)
                            correct_answer = question.correct_answer
                        else:
                            continue

                        if correct_answer and user_answer == correct_answer:
                            total_correct_answers += 1

                            # Save the user's answer in the database (UserAnswer model)
                            UserAnswer.objects.create(
                                test=test,
                                question_type=question_type,
                                question=question,
                                user=self.request.user,
                                user_answer=user_answer
                            )
                    except MatchingQuestion.DoesNotExist:
                        print(f"Matching question with ID {question_id} does not exist.")
                    except FillInTheBlanksQuestion.DoesNotExist:
                        print(f"Fill-in-the-blanks question with ID {question_id} does not exist.")
                    except MCQQuestion.DoesNotExist:
                        print(f"MCQ question with ID {question_id} does not exist.")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        return total_correct_answers