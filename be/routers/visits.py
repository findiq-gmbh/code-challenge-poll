from fastapi import APIRouter

from database import SessionDep
from schemas import QuestionWithVisits
import services.visits as visit_service

router = APIRouter(prefix="/visits", tags=["visits"])


@router.get("/", summary="List questions ordered by visit count")
def get_visit_counts(session: SessionDep) -> list[QuestionWithVisits]:
    return visit_service.get_visit_counts(session)
