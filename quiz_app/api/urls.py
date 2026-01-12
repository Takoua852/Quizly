"""URL routing for the quiz_app API endpoints."""

from rest_framework.urls import path
from .views import QuizViewDetail, CreateQuizView, QuizListView

urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name="create-quiz"),
    path('quizzes/', QuizListView.as_view(), name="quiz-list"),
    path('quizzes/<int:pk>/', QuizViewDetail.as_view(), name="quiz-detail")
]
