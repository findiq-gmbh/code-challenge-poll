from fastapi import APIRouter, HTTPException

from database import SessionDep
from models import Answer
import services.answers as answer_service

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = answer_service.get_answer(session, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer
