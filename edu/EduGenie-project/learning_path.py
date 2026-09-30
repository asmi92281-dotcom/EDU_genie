from gemini_client import get_gemini

def get_learning_recommendations(topic: str) -> str:
    prompt = f"""Create a personalized learning path for: {topic}

Structure it as:
1. Goal
2. Beginner foundations
3. Intermediate concepts
4. Advanced concepts
5. Suggested timeline (flexible)
6. Practice/project ideas
7. Resources to look for (types of resources such as official docs, books, videos, courses; do not invent URLs)
8. A simple weekly study routine

Make the sequence practical and learner-friendly. Keep it concise but useful."""
    return get_gemini().generate(prompt, temperature=0.4, max_output_tokens=1200)
