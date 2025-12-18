def build_quiz_prompt(transcript: str) -> str:
    """
   Build a strict prompt for the Gemini language model that enforces
   structured JSON output for quiz generation.

   The prompt instructs the model to:
   - Generate exactly 10 quiz questions
   - Use multiple-choice format with 4 options
   - Return raw JSON without additional text

   Args:
       transcript (str): Transcript text used as the knowledge source.

   Returns:
       str: Fully formatted prompt string for the LLM.
   """

    return f"""
You are a system that generates quiz questions strictly as JSON.

TASK:
Create EXACTLY 10 multiple-choice quiz questions based ONLY on the transcript below.

STRICT REQUIREMENTS (MUST FOLLOW ALL):
- Output MUST be a valid JSON array.
- The array MUST contain EXACTLY 10 objects.
- Each object MUST contain:
  - "question_title": a clear question between 40 and 70 characters.
  - "question_options": an array of EXACTLY 4 unique strings.
  - "answer": EXACTLY one string that matches one of the options.
- The correct answer MUST appear verbatim in "question_options".
- Do NOT repeat questions.
- Do NOT repeat answer options within a question.
- All questions MUST be directly derived from the transcript.
- Do NOT invent facts not present in the transcript.

OUTPUT RULES (CRITICAL):
- Output ONLY the raw JSON array.
- Do NOT include explanations.
- Do NOT include markdown.
- Do NOT include backticks.
- Do NOT include any text before or after the JSON.
- If you cannot fully comply, output NOTHING.

EXAMPLE FORMAT:
[
  {{
    "question_title": "Example question written clearly and precisely?",
    "question_options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

TRANSCRIPT:
{transcript}
"""
