from typing import Annotated, List
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    BackgroundTasks,
)
from pydantic import BaseModel, Field

from Model import Question
from Repository.question import QuestionRepository
from main import SessionDep

router = APIRouter()

# todo: it could make sense to move the models out, or to split the actions into seperate files
class CreateQuestionRequest(BaseModel):
    title: str = Field(..., max_length=1000, description="The title of the question")


class CreateQuestionResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for a question")


# todo: find a better name
class ListQuestionsResponse(BaseModel):
    title: str
    visitor_count: int


class ReadQuestionResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for a question")
    title: str = Field(..., description="The title of the question")


async def increment_visitor_count(question_id: int, session: SessionDep):
    question_repository = QuestionRepository(session)
    question_repository.increment_visitor_count(question_id)


@router.post("/questions", description="Add a new question", tags=["questions"])
def create_question(
    question: CreateQuestionRequest, session: SessionDep
) -> CreateQuestionResponse:
    session.add(Question(title=question.title))
    session.commit()
    session.refresh(question)
    session.close()
    return CreateQuestionResponse(id=question.id)


@router.get("/questions", description="Get a list of questions", tags=["questions"])
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[ListQuestionsResponse]:
    question_repository = QuestionRepository(session)
    questions = question_repository.get_questions(offset, limit)
    session.close()
    return [
        ListQuestionsResponse(
            title=question.title, visitor_count=question.visitor_count
        )
        for question in questions
    ]


@router.get(
    "/questions/{question_id}",
    description="Get a specific question",
    tags=["questions"],
)
def read_question(
    question_id: int, session: SessionDep, background_tasks: BackgroundTasks
) -> Question:
    question_repository = QuestionRepository(session)
    question = question_repository.get_question_by_id(question_id)

    if not question:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="question not found"
        )

    background_tasks.add_task(
        lambda: question_repository.increment_visitor_count(question_id, session)
    )

    session.close()
    return question
