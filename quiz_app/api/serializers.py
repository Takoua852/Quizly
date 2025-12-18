from rest_framework import serializers
from quiz_app.models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question model.

    Responsibilities:
    - Serialize and deserialize Question instances
    - Include fields: id, question_title, question_options, answer,
      created_at, updated_at
    - Remove created_at and updated_at from GET responses for cleaner output

    Example usage:
        serializer = QuestionSerializer(question_instance, context={'request': request})
        data = serializer.data
    """
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options",
                  "answer", "created_at", "updated_at"]

    def to_representation(self, instance):
        """
        Customize the serialized representation of a Question instance.

        Removes 'created_at' and 'updated_at' fields for GET requests.

        Args:
            instance (Question): Question model instance

        Returns:
            dict: Serialized representation of the question
        """
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.method == "GET":
            data.pop("created_at", None)
            data.pop("updated_at", None)
        return data


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz model.

    Responsibilities:
    - Serialize and deserialize Quiz instances
    - Include nested QuestionSerializer for associated questions
    - Include fields: id, title, description, created_at, updated_at,
      video_url, questions

    Example usage:
        serializer = QuizSerializer(quiz_instance)
        data = serializer.data
    """


    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description",
                  "created_at", "updated_at", "video_url", "questions"]
