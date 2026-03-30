from sqlmodel import Session, select

from models import Answer
from schemas import AnswerCreate


def create_answer(session: Session, question_id: int, data: AnswerCreate) -> Answer:
    answer = Answer(text=data.text, question_id=question_id)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


def get_answer(session: Session, answer_id: int) -> Answer | None:
    return session.get(Answer, answer_id)


def get_answers_by_question(
    session: Session, question_id: int, offset: int = 0, limit: int = 100
) -> list[Answer]:
    return list(
        session.exec(
            select(Answer)
            .where(Answer.question_id == question_id)
            .offset(offset)
            .limit(limit)
        ).all()
    )
