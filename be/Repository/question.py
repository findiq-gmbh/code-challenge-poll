from sqlmodel import select, text
from model import Question
from dependencies import SessionDep


class QuestionRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_questions(self, offset: int, limit: int):
        return self.session.exec(select(Question).offset(offset).limit(limit)).all()

    def get_question_by_id(self, question_id):
        return self.session.exec(
            select(Question).where(Question.id == question_id)
        ).first()

    def increment_visitor_count(self, question_id: int):
        query = text(
            "UPDATE question SET visitor_count = visitor_count + 1 WHERE id = :question_id"
        )
        self.session.exec(query.params(question_id=question_id))
        self.session.commit()
