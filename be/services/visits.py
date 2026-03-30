from sqlalchemy import func
from sqlmodel import Session, select

from models import Question, QuestionVisit
from schemas import QuestionWithVisits


def record_visit(session: Session, question_id: int) -> int:
    session.add(QuestionVisit(question_id=question_id))
    session.commit()
    visits = session.exec(
        select(QuestionVisit).where(QuestionVisit.question_id == question_id)
    ).all()
    return len(visits)


def get_visit_counts(session: Session) -> list[QuestionWithVisits]:
    stmt = (
        select(Question.id, Question.text, func.count(QuestionVisit.id).label("visit_count"))
        .outerjoin(QuestionVisit, Question.id == QuestionVisit.question_id)
        .group_by(Question.id)
        .order_by(func.count(QuestionVisit.id).desc())
    )
    rows = session.execute(stmt).all()
    return [QuestionWithVisits(id=row.id, text=row.text, visit_count=row.visit_count) for row in rows]
