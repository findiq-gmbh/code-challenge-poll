from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, Request, status
from pydantic import BaseModel, Field

from model import Answer
from repository.answer import AnswerRepository
from repository.question import QuestionRepository
from dependencies import SessionDep, limiter

router = APIRouter()


# todo: it could make sense to move the models out, or to split the actions into seperate files
class CreateAnswerRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="The text of the answer"
    )


class CreateAnswerResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")


class ReadAnswersResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")
    text: str = Field(..., description="The text of the answer")


class ReadAnswerResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")
    text: str = Field(..., description="The text of the answer")


@router.post(
    "/questions/{question_id}/answers",
    description="Create a new answer for a question",
    tags=["answers"],
)
@limiter.limit("5/minute")
def create_answer(
    request: Request,
    answer: CreateAnswerRequest,
    session: SessionDep,
    question_id: int = Path(..., description="The question id", ge=1),
) -> CreateAnswerResponse:
    question_repository = QuestionRepository(session)

    if question_repository.get_question_by_id(question_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="question not found"
        )

    answer = Answer(question_id=question_id, text=answer.text)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return CreateAnswerResponse(id=answer.id)


@router.get(
    "/questions/{question_id}/answers",
    description="Get a list of answers for ",
    tags=["answers"],
)
def read_answers_for_question(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)],
    limit: Annotated[int, Query(ge=1, le=100)],
    question_id: int = Path(..., description="The question id", ge=1),
) -> List[ReadAnswersResponse]:
    question_repository = QuestionRepository(session)

    if question_repository.get_question_by_id(question_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="question not found"
        )

    answer_repository = AnswerRepository(session)

    return [
        ReadAnswersResponse(id=answer.id, text=answer.text)
        for answer in answer_repository.get_answers_by_question(
            question_id, offset, limit
        )
    ]


# todo: idk the best practise for it, have to figure out later
@router.get(
    "/answers",
    description="Get all answers",
    tags=["answers"],
 )
def read_answers(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)],
    limit: Annotated[int, Query(ge=1, le=100)],
 ) -> List[ReadAnswerResponse]:
    answer_repository = AnswerRepository(session)
    answers = answer_repository.get_all_answers(offset, limit)
    return [ReadAnswerResponse(id=answer.id, text=answer.text) for answer in answers]
