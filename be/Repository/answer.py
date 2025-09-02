from sqlmodel import select
from model import Answer
from dependencies import SessionDep


class AnswerRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_answer(self, text, question_id):
        answer = Answer(text=text, question_id=question_id)
        self.session.add(answer)
        self.session.commit()
        self.session.refresh(answer)
        return answer

    def get_answers_by_question(self, question_id: int, offset: int, limit: int):
        return self.session.exec(
            select(Answer)
            .where(Answer.question_id == question_id)
            .offset(offset)
            .limit(limit)
        ).all()

    def get_answer_by_id(self, answer_id: int):
        return self.session.get(Answer, answer_id)

    def get_all_answers(self, offset: int, limit: int):
        return self.session.exec(
            select(Answer)
            .offset(offset)
            .limit(limit)
        ).all()
