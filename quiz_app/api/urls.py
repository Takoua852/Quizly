"""
urls.py

Defines URL routing for the quiz_app API endpoints.

Endpoints:
    - POST /createQuiz/       : Create a new quiz from a YouTube URL
    - GET /quizzes/           : List all quizzes belonging to the authenticated user
    - GET/PUT/PATCH/DELETE /quizzes/<pk>/ : Retrieve, update, or delete a specific quiz

Usage:
    Include this module in the project's main urls.py using Django's `include`.
"""
from rest_framework.urls import path
from .views import QuizViewDetail, CreateQuizView, QuizListView

urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name="create-quiz"),
    path('quizzes/', QuizListView.as_view(), name="quiz-list"),
    path('quizzes/<int:pk>/', QuizViewDetail.as_view(), name="quiz-detail")
]
