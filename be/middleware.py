from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


def register_middleware(app: FastAPI) -> None:
    origins = ["*"] if not settings.is_production else [settings.frontend_url]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
