from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from quiz_app.models import Quiz, Question
from unittest.mock import patch

User = get_user_model()


class QuizTests(TestCase):
    """Test CRUD operations for Quiz and Question endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="quizuser", email="quiz@example.com", password="pass123"
        )
        self.client.force_authenticate(user=self.user)

    @patch("quiz_app.services.quiz_creator.QuizCreator.create")
    def test_create_quiz_success(self, mock_create):
        """Create a new quiz successfully."""
        # Mock the QuizCreator to avoid actual YouTube download & Whisper
        quiz = Quiz.objects.create(
            user=self.user,
            title="Test Quiz",
            description="Test Description",
            video_url="https://youtu.be/testvideo"
        )
        Question.objects.create(
            quiz=quiz,
            question_title="Q1",
            question_options=["A", "B", "C", "D"],
            answer="A"
        )
        mock_create.return_value = quiz

        response = self.client.post("/api/createQuiz/", {"url": "https://youtu.be/testvideo"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Quiz")
        self.assertEqual(len(response.data["questions"]), 1)

    def test_list_quizzes(self):
        """List all quizzes of the authenticated user."""
        Quiz.objects.create(
            user=self.user,
            title="My Quiz",
            description="Desc",
            video_url="https://youtu.be/test1"
        )
        response = self.client.get("/api/quizzes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "My Quiz")

    def test_quiz_detail_retrieve(self):
        """Retrieve a single quiz with questions."""
        quiz = Quiz.objects.create(
            user=self.user,
            title="Detail Quiz",
            description="Desc",
            video_url="https://youtu.be/test2"
        )
        Question.objects.create(
            quiz=quiz,
            question_title="Q1",
            question_options=["A", "B", "C", "D"],
            answer="B"
        )
        response = self.client.get(f"/api/quizzes/{quiz.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detail Quiz")
        self.assertEqual(len(response.data["questions"]), 1)

    def test_quiz_update(self):
        """Update quiz title and description."""
        quiz = Quiz.objects.create(
            user=self.user,
            title="Old Title",
            description="Old Desc",
            video_url="https://youtu.be/test3"
        )
        payload = {"title": "New Title", "description": "New Desc"}
        response = self.client.patch(f"/api/quizzes/{quiz.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quiz.refresh_from_db()
        self.assertEqual(quiz.title, "New Title")
        self.assertEqual(quiz.description, "New Desc")

    def test_quiz_delete(self):
        """Delete a quiz."""
        quiz = Quiz.objects.create(
            user=self.user,
            title="Delete Quiz",
            description="Desc",
            video_url="https://youtu.be/test4"
        )
        response = self.client.delete(f"/api/quizzes/{quiz.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Quiz.objects.filter(id=quiz.id).exists())