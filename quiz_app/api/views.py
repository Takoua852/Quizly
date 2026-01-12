from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuizSerializer
from .permissions import IsOwner
from quiz_app.models import Quiz
from quiz_app.services.quiz_creator import QuizCreator


class QuizViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single Quiz. Only the owner can access."""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class QuizListView(APIView):
    """List all quizzes belonging to the authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

    def get(self, request):
        serializer = QuizSerializer(
            self.get_queryset(), many=True, context={"request": request})
        return Response(serializer.data)


class CreateQuizView(APIView):
    """Create a quiz from a YouTube video. Authenticated users only."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

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
