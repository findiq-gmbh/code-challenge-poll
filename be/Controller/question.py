from typing import Annotated, List
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    Request,
    status,
    BackgroundTasks,
)
from pydantic import BaseModel, Field

from model import Question
from repository.question import QuestionRepository
from dependencies import SessionDep, limiter

router = APIRouter()


# todo: it could make sense to move the models out, or to split the actions into seperate files
class CreateQuestionRequest(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=1000, description="The title of the question"
    )


class CreateQuestionResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for a question")


# todo: find a better name
class ListQuestionsResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for a question")
    title: str = Field(..., description="The title of the question")
    visitor_count: int = Field(
        ..., description="The number of visitors to the question"
    )


class ReadQuestionResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for a question")
    title: str = Field(..., description="The title of the question")


async def increment_visitor_count(question_id: int, session: SessionDep):
    question_repository = QuestionRepository(session)
    question_repository.increment_visitor_count(question_id)


@router.post("/questions", description="Add a new question", tags=["questions"])
@limiter.limit("5/minute")
def create_question(
    request: Request,
    session: SessionDep,
    question: CreateQuestionRequest,
) -> CreateQuestionResponse:
    db_question = Question(title=question.title)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    session.close()
    return CreateQuestionResponse(id=db_question.id)


@router.get("/questions", description="Get a list of questions", tags=["questions"])
def read_questions(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)],
    limit: Annotated[int, Query(ge=1, le=100)],
) -> List[ListQuestionsResponse]:
    question_repository = QuestionRepository(session)
    questions = question_repository.get_questions(offset, limit)
    session.close()
    return [
        ListQuestionsResponse(
            id=question.id, title=question.title, visitor_count=question.visitor_count
        )
        for question in questions
    ]


@router.get(
    "/questions/{question_id}",
    description="Get a specific question",
    tags=["questions"],
)
def read_question(
    session: SessionDep,
    background_tasks: BackgroundTasks,
    question_id: int = Path(
        ..., description="Get the information for a specific question", ge=1
    ),
) -> Question:
    question_repository = QuestionRepository(session)
    question = question_repository.get_question_by_id(question_id)

    if not question:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="question not found"
        )

    background_tasks.add_task(
        increment_visitor_count, question_id=question_id, session=session
    )

    session.close()
    return question
