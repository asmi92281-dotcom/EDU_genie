from pydantic import BaseModel, Field, field_validator

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input text cannot be empty.")
        return value

class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""

class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
