from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, get_session
from routers import questions, answers

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
    
app = FastAPI(lifespan=lifespan)

app.include_router(questions.router)
app.include_router(answers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='http://localhost:\d+$',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionDep = Annotated[Session, Depends(get_session)]



