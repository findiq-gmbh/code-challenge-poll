from contextlib import asynccontextmanager
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine

from Enum.app_environment import AppEnvironmentEnum
from Controller import answer, question

app = FastAPI()

# todo: replace later by a environment configuratrion
database_connection_string = f"sqlite:///database.db"

connect_args = {"check_same_thread": False}
engine = create_engine(database_connection_string, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session




@asynccontextmanager
async def lifespan(app: FastAPI):
    if env != AppEnvironmentEnum.DEVELOPMENT:
        return
    create_db_and_tables()
    yield
    engine.dispose(close=True)


SessionDep = Annotated[Session, Depends(get_session)]

# todo: extract later to a env config loader
env = os.getenv("app_environment", AppEnvironmentEnum.DEVELOPMENT)
app = FastAPI(
    debug=env == AppEnvironmentEnum.DEVELOPMENT,
    docs_url="/docs" if env == AppEnvironmentEnum.DEVELOPMENT else None,
    redoc_url="/redoc" if env == AppEnvironmentEnum.DEVELOPMENT else None,
    lifespan=lifespan
)
app.include_router(question.router)
app.include_router(answer.router)
