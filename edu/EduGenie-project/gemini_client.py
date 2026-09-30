from functools import lru_cache
from google.genai import types
from config import get_settings

class GeminiService:
    def __init__(self) -> None:
        from google import genai
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env before using AI features.")
        self.model = settings.gemini_model
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate(self, prompt: str, *, temperature: float = 0.4, max_output_tokens: int = 1200) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

@lru_cache
def get_gemini() -> GeminiService:
    return GeminiService()
