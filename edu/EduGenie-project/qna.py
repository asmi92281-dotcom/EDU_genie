from gemini_client import get_gemini

def answer_question(question: str) -> str:
    prompt = f"""You are EduGenie, a reliable educational Q&A assistant.
Answer the student's question clearly and concisely.
Question: {question}

Rules:
- Give the direct answer first.
- Explain the reasoning or key facts briefly.
- If the question is ambiguous, state the assumption you used.
- Do not invent citations, facts, or sources.
- Keep the answer suitable for a learner."""
    return get_gemini().generate(prompt, temperature=0.2, max_output_tokens=700)
