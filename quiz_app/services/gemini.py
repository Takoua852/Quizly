import json
import re
from google import genai
from django.conf import settings
from .prompts import build_quiz_prompt
from .validators import is_valid_quiz_payload

client = genai.Client(api_key=settings.GOOGLE_GENAI_API_KEY)


class GeminiQuizService:
    """
      Service class responsible for generating quiz questions using
      the Google Gemini language model.

      The service takes a transcript as input and attempts to generate
      exactly 10 multiple-choice quiz questions that strictly follow
      a predefined JSON schema.

      Responsibilities:
      - Build and send prompts to the Gemini API
      - Retry generation on invalid or malformed responses
      - Validate the generated quiz structure before returning data

      Raises:
          RuntimeError: If a valid quiz cannot be generated after
                        the configured number of retries.
      """

    @staticmethod
    def generate_questions(transcript: str, retries=5):
        """
        Generate quiz questions from a transcript using Gemini.

        Args:
            transcript (str): Full transcript text extracted from a video.
            retries (int): Number of retry attempts if the response
                           is invalid or incomplete.

        Returns:
            list: A list of 10 validated quiz question dictionaries.

        Raises:
            RuntimeError: If Gemini fails to produce a valid result.
        """
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
