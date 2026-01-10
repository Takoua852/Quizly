from quiz_app.models import Quiz, Question
from quiz_app.utils import extract_video_id
from .youtube import YouTubeService
from .transcription import TranscriptionService
from .gemini import GeminiQuizService
from django.db import transaction

class QuizCreator:
    """
    High-level service class to orchestrate the creation of a Quiz
    from a YouTube video.

    Responsibilities:
    - Validate and normalize YouTube URLs
    - Download and transcribe video audio
    - Generate quiz questions using Gemini
    - Persist Quiz and associated Questions in the database

    Example usage:
        quiz = QuizCreator.create(user, "https://youtu.be/example")
    """

    @staticmethod
    def create(user, youtube_url: str) -> Quiz:

        """
        Create a Quiz from a YouTube video URL.

        Workflow:
        1. Extract video ID from the URL
        2. Create a Quiz instance with placeholder title/description
        3. Download audio using YouTubeService
        4. Transcribe audio using TranscriptionService
        5. Generate quiz questions using GeminiQuizService
        6. Save questions and update Quiz title/description

        Args:
            user (User): Django user who owns the quiz.
            youtube_url (str): Full YouTube video URL.

        Returns:
            Quiz: The created Quiz instance with all questions.

        Raises:
            RuntimeError: If the YouTube URL is invalid or
                          quiz generation fails at any stage.
        """
        
        video_id = extract_video_id(youtube_url)
        if not video_id:
            raise RuntimeError("Ungültige YouTube-URL")

        clean_url = f"https://www.youtube.com/watch?v={video_id}"

        with transaction.atomic():
     
            quiz = Quiz.objects.create(
                user=user,
                title="Quiz wird erstellt...",
                description="Transkription läuft...",
                video_url=clean_url
            )

        audio, info = YouTubeService.download_audio(clean_url)
        transcript = TranscriptionService.transcribe(audio)
        questions = GeminiQuizService.generate_questions(transcript)

        for q in questions:
            Question.objects.create(
                quiz=quiz,
                question_title=q["question_title"],
                question_options=q["question_options"],
                answer=q["answer"]
            )

        quiz.title = info.get("title", "Neues Quiz")
        quiz.description = info.get("description", "")
        quiz.save()

        return quiz
