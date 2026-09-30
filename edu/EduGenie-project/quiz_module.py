from gemini_client import get_gemini
from schemas import QuizResponse
from utils import parse_json


def generate_quiz(text: str) -> QuizResponse:
    prompt = f"""Create exactly 3 multiple-choice questions from the educational content below.
Return ONLY valid JSON matching this shape:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "exactly one option string from options",
      "explanation": "brief reason"
    }}
  ]
}}

Content:
{text}
"""
    raw = get_gemini().generate(prompt, temperature=0.2, max_output_tokens=1000)
    try:
        data = parse_json(raw)
        if isinstance(data, list):
            data = {"questions": data}
        result = QuizResponse.model_validate(data)
        for item in result.questions:
            if item.correct_answer not in item.options:
                raise ValueError("correct_answer must match one of the options")
        if len(result.questions) != 3:
            raise ValueError("Expected exactly 3 questions")
        return result
    except Exception as exc:
        raise RuntimeError(f"Quiz JSON could not be parsed or validated: {exc}") from exc
