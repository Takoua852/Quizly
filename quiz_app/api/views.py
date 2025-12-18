from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuizSerializer
from .permissions import IsOwner
from quiz_app.models import Quiz
from quiz_app.services.quiz_creator import QuizCreator


class QuizViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single Quiz instance.

    Permissions:
        - User must be authenticated
        - User must be the owner of the quiz (IsOwner)

    HTTP methods:
        GET: Retrieve quiz details including associated questions
        PUT/PATCH: Update quiz fields (title, description, etc.)
        DELETE: Delete the quiz
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class QuizListView(APIView):
    """
    API endpoint to list all quizzes belonging to the authenticated user.

    Permissions:
        - User must be authenticated

    HTTP methods:
        GET: Return a list of quizzes owned by the current user, including
             all associated questions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

    def get(self, request):
        serializer = QuizSerializer(
            self.get_queryset(), many=True, context={"request": request})
        return Response(serializer.data)


class CreateQuizView(APIView):
    """
    API endpoint for creating a quiz from a YouTube video.

    Workflow:
    - Accept a YouTube URL from the client
    - Extract and normalize the video ID
    - Download and transcribe audio using Whisper
    - Generate quiz questions using Gemini
    - Persist quiz and questions in the database

    Permissions:
        - User must be authenticated
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle quiz creation request.

        Expects:
            JSON body with key 'url' containing a YouTube video URL.

        Returns:
            Response:
                - 201: Quiz created successfully
                - 400: Invalid or missing URL
                - 500: Internal processing error
        """
        url = request.data.get("url")
        if not url:
            return Response({"error": "YouTube URL required"}, status=400)

        try:
            quiz = QuizCreator.create(request.user, url)
            quiz.refresh_from_db()
            return Response(
                QuizSerializer(quiz, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
