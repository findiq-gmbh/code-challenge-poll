from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, Query
from sqlmodel import Session, select

from models import Answer, Question
from schemas import AnswerCreate
from database import get_session
from starlette import status

router = APIRouter(
    tags=['answer']
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/answers/", status_code=status.HTTP_201_CREATED)
def create_answer(answer: AnswerCreate, session: SessionDep) -> Answer:
    question = session.exec(select(Question).where(answer.question_id == Question.id)).first()
    if not question:
        raise HTTPException(status_code=401, detail='no question found for the provided question id')
    
    db_answer = Answer.model_validate(answer)
    session.add(db_answer)
    session.commit()
    session.refresh(db_answer)
    return db_answer