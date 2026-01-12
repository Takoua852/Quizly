import json
import re
from google import genai
from django.conf import settings
from .prompts import build_quiz_prompt
from .validators import is_valid_quiz_payload

client = genai.Client(api_key=settings.GOOGLE_GENAI_API_KEY)


class GeminiQuizService:
    """Service to generate 10 multiple-choice quiz questions from a transcript using Gemini."""


    @staticmethod
    def generate_questions(transcript: str, retries=5):
        """Generate validated quiz questions from transcript text."""

        prompt = build_quiz_prompt(transcript)

        for _ in range(retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                text = response.text.strip()
                match = re.search(r"\[[\s\S]*\]", text)
                if not match:
                    continue

                data = json.loads(match.group(0))
                if is_valid_quiz_payload(data):
                    return data

            except Exception:
                continue

        raise RuntimeError("Gemini failed")
