"""
models.py

Defines the data models for the quiz_app.

Models:
    - Quiz: Represents a quiz created by a user, linked to a YouTube video.
    - Question: Represents a single multiple-choice question belonging
      to a Quiz, including options and the correct answer.

Relationships:
    - Quiz has a ForeignKey to the User model.
    - Question has a ForeignKey to Quiz.
"""
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Quiz(models.Model):
    """
    Model representing a quiz.

    Attributes:
        user (ForeignKey): The user who created the quiz.
        title (str): Title of the quiz.
        description (str): Optional description of the quiz.
        video_url (str): URL of the associated YouTube video.
        created_at (datetime): Timestamp when the quiz was created.
        updated_at (datetime): Timestamp when the quiz was last updated.

    Relationships:
        - One user can have many quizzes (related_name='quizzes')
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):

    """
    Model representing a multiple-choice question.

    Attributes:
        quiz (ForeignKey): The quiz to which this question belongs.
        question_title (str): The text of the question.
        question_options (list): A list of 4 possible answer options.
        answer (str): The correct answer, must match one of the options.
        created_at (datetime): Timestamp when the question was created.
        updated_at (datetime): Timestamp when the question was last updated.

    Relationships:
        - Each question belongs to one quiz (related_name='questions')
    """

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')

    question_title = models.CharField(max_length=500)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.title} – {self.question_title}"
