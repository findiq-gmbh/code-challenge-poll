from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from Model import Answer
from Repository.answer import AnswerRepository
from Repository.question import QuestionRepository
from main import SessionDep

router = APIRouter()

# todo: it could make sense to move the models out, or to split the actions into seperate files
class CreateAnswerRequest(BaseModel):
    text: str = Field(..., max_length=10000, description="The text of the answer")

class CreateAnswerResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")

class ReadAnswersResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")
    text: str = Field(..., description="The text of the answer")

class ReadAnswerResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the answer")
    text: str = Field(..., description="The text of the answer")

@router.post("/questions/{question_id}/answers", description="Create a new answer for a question", tags=["answers"])
def create_answer(answer: CreateAnswerRequest, session: SessionDep, question_id: int = Path(..., description="The question id")) -> CreateAnswerResponse:
    question_repository = QuestionRepository(session)

    if(question_repository.get_question_by_id(question_id) is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="question not found")

    answer = Answer(question_id=question_id, text=answer.text)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return CreateAnswerResponse(id=answer.id)


@router.get("/questions/{question_id}/answers", description="Get a list of answers for ", tags=["answers"])
def read_answers_for_question(
    question_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[ReadAnswersResponse]:
    question_repository = QuestionRepository(session)

    if(question_repository.get_question_by_id(question_id) is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="question not found")

    answer_repository = AnswerRepository(session)

    return answer_repository.get_answers_by_question(question_id, offset, limit)


# todo: idk the best practise for it, have to figure out later
@router.get("/questions/answers/{answer_id}", description="Get a specific answer by id", tags=["answers"])
def read_answer(answer_id: int, session: SessionDep) -> ReadAnswerResponse:
    answer_repository = AnswerRepository(session)
    answer = answer_repository.get_answer_by_id(answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="answer not found")
    return ReadAnswerResponse(id=answer.id, text=answer.text)
