from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Quiz(models.Model):
    
    """Represents a quiz created by a user, linked to a YouTube video."""

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
    
    """Represents a multiple-choice question belonging to a Quiz."""

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')

    question_title = models.CharField(max_length=500)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.title} – {self.question_title}"
