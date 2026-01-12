from quiz_app.models import Quiz, Question
from quiz_app.utils import extract_video_id
from .youtube import YouTubeService
from .transcription import TranscriptionService
from .gemini import GeminiQuizService
from django.db import transaction

class QuizCreator:
    """Orchestrates creating a Quiz from a YouTube video."""

    @staticmethod
    def create(user, youtube_url: str) -> Quiz:
        video_id = QuizCreator._extract_video_id(youtube_url)
        clean_url = f"https://www.youtube.com/watch?v={video_id}"

        quiz = QuizCreator._create_quiz_placeholder(user, clean_url)
        transcript, info = QuizCreator._download_and_transcribe(clean_url)
        questions = GeminiQuizService.generate_questions(transcript)
        QuizCreator._save_questions(quiz, questions)
        QuizCreator._update_quiz_info(quiz, info)

        return quiz

    @staticmethod
    def _extract_video_id(url: str) -> str:
        video_id = extract_video_id(url)
        if not video_id:
            raise RuntimeError("Ungültige YouTube-URL")
        return video_id

    @staticmethod
    def _create_quiz_placeholder(user, url) -> Quiz:
        with transaction.atomic():
            return Quiz.objects.create(
                user=user,
                title="Quiz wird erstellt...",
                description="Transkription läuft...",
                video_url=url
            )

    @staticmethod
    def _download_and_transcribe(url):
        audio, info = YouTubeService.download_audio(url)
        transcript = TranscriptionService.transcribe(audio)
        return transcript, info

    @staticmethod
    def _save_questions(quiz, questions):
        for q in questions:
            Question.objects.create(
                quiz=quiz,
                question_title=q["question_title"],
                question_options=q["question_options"],
                answer=q["answer"]
            )

    @staticmethod
    def _update_quiz_info(quiz, info):
        quiz.title = info.get("title", "Neues Quiz")
        quiz.description = ""
        quiz.save()

