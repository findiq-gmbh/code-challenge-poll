from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from database import SessionDep
from models import Answer, Question
from schemas import AnswerCreate, QuestionCreate
import services.answers as answer_service
import services.questions as question_service
import services.visits as visit_service

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", status_code=201)
def create_question(data: QuestionCreate, session: SessionDep) -> Question:
    return question_service.create_question(session, data)


@router.get("/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    return question_service.get_questions(session, offset, limit)


@router.get("/{question_id}")
def read_question(question_id: int, session: SessionDep) -> Question:
    question = question_service.get_question(session, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/{question_id}/answers", tags=["answers"])
def read_answers_for_question(
    question_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Answer]:
    question = question_service.get_question(session, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return answer_service.get_answers_by_question(session, question_id, offset, limit)


@router.post("/{question_id}/visit", status_code=201, tags=["visits"])
def record_visit(question_id: int, session: SessionDep) -> dict:
    question = question_service.get_question(session, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    count = visit_service.record_visit(session, question_id)
    return {"count": count}


@router.post("/{question_id}/answers", status_code=201, tags=["answers"])
def create_answer_for_question(
    question_id: int,
    data: AnswerCreate,
    session: SessionDep,
) -> Answer:
    question = question_service.get_question(session, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return answer_service.create_answer(session, question_id, data)
