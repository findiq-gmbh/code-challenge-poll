import os

from slowapi import Limiter
from enums.app_environment import AppEnvironmentEnum
from dotenv import load_dotenv

from enums.environment_name import EnvironmentNameEnum

env = os.getenv(
    EnvironmentNameEnum.APP_ENVIRONMENT.value, AppEnvironmentEnum.DEVELOPMENT.value
)
load_dotenv(dotenv_path=f".{env}.env")

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from controller import answer, question
from dependencies import engine, limiter
from model import *  # noqa: F401


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if env not in [AppEnvironmentEnum.DEVELOPMENT, AppEnvironmentEnum.TESTING]:
        return
    create_db_and_tables()
    yield
    engine.dispose(close=True)


# todo: extract later to a env config loader
app = FastAPI(
    debug=env == AppEnvironmentEnum.DEVELOPMENT,
    docs_url="/docs" if env == AppEnvironmentEnum.DEVELOPMENT else None,
    redoc_url="/redoc" if env == AppEnvironmentEnum.DEVELOPMENT else None,
    lifespan=lifespan,
)
app.include_router(question.router)
app.include_router(answer.router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


if env == AppEnvironmentEnum.DEVELOPMENT.value:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__" and env == AppEnvironmentEnum.DEVELOPMENT:
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes=["polling/**"],
    )
