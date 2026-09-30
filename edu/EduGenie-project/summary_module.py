from gemini_client import get_gemini

def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational passage for quick revision.
Keep the important facts, concepts, relationships, and conclusions.
Use short paragraphs or bullet points where helpful.
Do not add information that is not present in the passage.

Passage:
{text}"""
    return get_gemini().generate(prompt, temperature=0.2, max_output_tokens=900)
