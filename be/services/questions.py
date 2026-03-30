from sqlmodel import Session, select

from models import Question
from schemas import QuestionCreate


def create_question(session: Session, data: QuestionCreate) -> Question:
    question = Question(text=data.text)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def get_question(session: Session, question_id: int) -> Question | None:
    return session.get(Question, question_id)


def get_questions(session: Session, offset: int = 0, limit: int = 100) -> list[Question]:
    return list(session.exec(select(Question).offset(offset).limit(limit)).all())
