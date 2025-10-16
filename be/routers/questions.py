from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, Query
from sqlmodel import Session, select
from schemas import AnswerCreate, AnswersWithQuestion, QuestionCreate
from database import get_session
from models import Question, Answer
from starlette import status
router = APIRouter(
    tags=['questions']
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/questions/", response_model=Question, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, session: SessionDep) -> Question:
    db_question = Question.model_validate(question)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.get("/questions/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    questions = session.exec(select(Question).offset(offset).limit(limit)).all()
    return [*questions]


@router.get("/questions/{question_id}")
def read_question(session: SessionDep, question_id: int = Path(gt=0)) -> Question:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


@router.get("/questions/{question_id}/answers")
def read_answers(session: SessionDep, question_id:int = Path(gt=0),offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 100,) -> AnswersWithQuestion:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")

    answers = session.exec(
        select(Answer)
        .where(Answer.question_id == question_id)
        .offset(offset)
        .limit(limit)
    ).all()
    
    answer_with_question = AnswersWithQuestion(
        question_text=question.text,
        answers=answers
    )
    return answer_with_question

@router.patch("/questions/{question_id}/views")
def increment_views(session:SessionDep,question_id:int = Path(gt=0)):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    
    question.views += 1
    session.add(question)
    session.commit()
    session.refresh(question)
    return {"question_id": question.id, "views": question.views}
