import os
from typing import Annotated, Any, Union
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Session, create_engine, select, func

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://frontend",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(SQLModel, table=True):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("text"),)

    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Answer(SQLModel, table=True):
    __tablename__ = "answers"

    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="questions.id")
    text: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuestionVisit(SQLModel, table=True):
    __tablename__ = "question_visits"

    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="questions.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: str | None = Field(default=None)


sqlite_file_name = "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    os.makedirs("data", exist_ok=True)
    create_db_and_tables()

@app.post("/questions/")
def create_question(question: Question, session: SessionDep) -> Question:
    if not question.text or not question.text.strip():
        raise HTTPException(status_code=422, detail="question text cannot be empty")

    existing_question = session.exec(
        select(Question).where(Question.text == question.text)
    ).first()
    
    if existing_question:
        raise HTTPException(status_code=409, detail="question already exists")
    
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@app.get("/questions/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    questions = session.exec(select(Question).offset(offset).limit(limit)).all()
    return [*questions]


@app.get("/question/{question_id}")
def read_question(question_id: int, session: SessionDep) -> Question:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


@app.get("/question/{question_id}/answers")
def read_question_answers(question_id: int, session: SessionDep) -> list[Answer]:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    
    answers = session.exec(
        select(Answer).where(Answer.question_id == question_id)
    ).all()
    return [*answers]


@app.post("/answers/")
def create_answer(answer: Answer, session: SessionDep) -> Answer:
    question = session.get(Question, answer.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    
    if not answer.text or not answer.text.strip():
        raise HTTPException(status_code=422, detail="answer text cannot be empty")
    
    existing_answer = session.exec(
        select(Answer).where(
            (Answer.text == answer.text.strip()) & 
            (Answer.question_id == answer.question_id)
        )
    ).first()
    
    if existing_answer:
        raise HTTPException(status_code=409, detail="answer already exists for this question")
    
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


@app.get("/answer/{answer_id}")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    return answer


@app.post("/question/{question_id}/visit")
def track_question_visit(question_id: int, request: Request, session: SessionDep) -> QuestionVisit:

    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    
    client_ip = request.client.host if request.client else None
    
    visit = QuestionVisit(
        question_id=question_id,
        ip_address=client_ip
    )
    
    session.add(visit)
    session.commit()
    return visit


@app.get("/questions/visits")
def get_questions_visits(session: SessionDep) -> list[dict]:
    result = session.exec(
        select(
            Question.id,
            Question.text,
            func.count(QuestionVisit.id).label("visit_count")
        )
        .outerjoin(QuestionVisit, Question.id == QuestionVisit.question_id)
        .group_by(Question.id, Question.text)
        .order_by(func.count(QuestionVisit.id).desc())
    ).all()
    
    return [
        {
            "question_id": row.id,
            "question_text": row.text,
            "visit_count": row.visit_count
        }
        for row in result
    ]