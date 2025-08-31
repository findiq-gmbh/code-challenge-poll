from typing import Annotated, Any, Union
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, Session, create_engine, select

# Feedback: To be able to talk to the API, you need to implement CORS handling. Remember that you need a configuration for different environments.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Suggestion: Move models to a differnt file for a better structuring and overview in this file.
class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    answer_view_count: int = Field(default=0)

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    text: str = Field(index=True) # Feedback: Why have you defined `text` with an index?

# Suggestion: How is this ment to be handled in PROD? Maybe consider another database like PostgreSQL or MySQL.
#             You can add a DB with Docker and keep this handling out of the application code.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Feedback: Maybe you want to have a bit more control over the database creation process.
# Suggestion: Move this handling to a separate file. Maybe you want to call it explicitly in the CI/CD.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Suggestion: Move this to a separate file related to database initialization.
def initialize_database():
    create_db_and_tables()

# Suggestion: Move this to a separate file related to database session management.
def get_session():
    with Session(engine) as session:
        yield session

# Suggestion: Move this to a separate file related to database session management.
SessionDep = Annotated[Session, Depends(get_session)]

# Feedback: This might not be needed within the server application, since you could expect that a database is already initialized.
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/question/")
def create_question(question: Question, session: SessionDep) -> Question:
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


# Feedback: `session.exec().all()` is returning `Sequence[Question]` and can be returned directly.
#           No need to spread values of `Sequence[Question]` into a list.
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
        # Feedback: Can `404` be used out of a constant?
        raise HTTPException(status_code=404, detail="question not found")
    return question

@app.patch("/question/{question_id}/increase_answer_view_count")
def increase_question_answer_view_count(question_id: int, session: SessionDep):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    question.answer_view_count += 1
    session.add(question)
    session.commit()
    session.refresh(question)
    return question

@app.get("/questions")
def read_all_questions(session: SessionDep):
    return session.exec(select(Question)).all()

# Feedback: Currently there is no validation on the `Answer` object, which is sent by the client.
#           If you provide an ID within the `Answer` object, it will fail due to duplicate key constraint from the DB.
@app.post("/answer/")
def create_answer(answer: Answer, session: SessionDep) -> Answer:
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


# Feedback: Currently there are two use cases:
#           * Loading all answers (Main navigation, since you don't know the question ID from the navigation)
#           * Loading answers by question ID (from questions page)
#
# Suggestion: Adding a new endpoint to load answers by question ID
# Feedback: `session.exec().all()` returns a `Sequence[Answer]` that could be returned directly. The spreading into a list is not necessary.
#           Sometimes it can be useful to pass `session.exec().all()` into a variable and return the variable (e.g.debugging).
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
        # Feedback: `200` is an incorrect status code, if entity was not found. `404` is correct, like in `read_question()`
        raise HTTPException(status_code=200, detail="answer not found")
    return answer
