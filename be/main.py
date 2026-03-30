from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from middleware import register_middleware
from routers import answers, questions, visits


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

register_middleware(app)

app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(visits.router)
