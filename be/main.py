from typing import Annotated, Any, Union
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(index=True)

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    text: str = Field(index=True)

class AnswerVisits(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    visits: int = Field(index=True)

sqlite_file_name = "database.db"
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
    create_db_and_tables()

@app.post("/question/")
def create_question(question: Question, session: SessionDep) -> Question:
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@app.get("/question/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    question = session.exec(select(Question).offset(offset).limit(limit)).all()
    return [*question]


@app.get("/question/{question_id}")
def read_question(question_id: int, session: SessionDep) -> Question:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


@app.post("/answer/")
def create_answer(answer: Answer, session: SessionDep) -> Answer:
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


@app.get("/answer/")
def read_answers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Answer]:
    answer = session.exec(select(Answer).offset(offset).limit(limit)).all()
    return [*answer]


@app.get("/answer/{answer_id}")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    return answer

@app.get("/answer/{answer_id}")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    return answer


@app.put("/visits/{question_id}")
def update_visits(question_id: int, session: SessionDep) -> AnswerVisits:
    visits = session.query(AnswerVisits).filter(AnswerVisits.question_id == question_id).first()
    if visits:
        visits.visits += 1
    else:
        visits = AnswerVisits(question_id=question_id, visits=1)
        session.add(visits)

    session.commit()
    session.refresh(visits)
    return visits