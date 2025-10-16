from sqlmodel import Field, SQLModel

from models import Answer

class QuestionCreate(SQLModel):
    text: str = Field(min_length=1,description="The question text")

class AnswerCreate(SQLModel):
    question_id: int = Field(gt=0, description="The question ID must be greater than 0.")
    text: str = Field(min_length=1,description="The answer text")


class AnswersWithQuestion(SQLModel):
    question_text: str
    answers: list[Answer]