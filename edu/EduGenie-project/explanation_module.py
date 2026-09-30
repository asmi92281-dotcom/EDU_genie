from config import get_settings
from gemini_client import get_gemini

_local_pipeline = None


def _local_explain(topic: str) -> str:
    global _local_pipeline
    try:
        if _local_pipeline is None:
            from transformers import pipeline
            _local_pipeline = pipeline("text2text-generation", model=get_settings().local_explanation_model)
        prompt = f"Explain the following educational topic simply for a beginner: {topic}"
        result = _local_pipeline(prompt, max_new_tokens=220, do_sample=False)
        return result[0]["generated_text"].strip()
    except Exception as exc:
        raise RuntimeError(f"Local explanation model could not run: {exc}") from exc


def explain_topic(topic: str) -> str:
    settings = get_settings()
    if settings.explanation_backend.lower() == "local":
        return _local_explain(topic)
    prompt = f"""You are EduGenie, an educational assistant. Explain this topic to a beginner.
Topic: {topic}

Requirements:
- Use simple language.
- Start with a one-sentence definition.
- Give a short intuitive explanation.
- Give one everyday or practical example.
- Avoid unnecessary jargon.
- Keep it concise (about 150-250 words)."""
    return get_gemini().generate(prompt, temperature=0.3, max_output_tokens=500)
