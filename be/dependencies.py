from typing import Annotated
from fastapi import Depends
from slowapi import Limiter
from sqlmodel import Session, create_engine
from slowapi.util import get_remote_address

import os

limiter = Limiter(key_func=get_remote_address)

# todo: replace later by a environment configuratrion
database_connection_string = os.getenv(
    "DATABASE_CONNECTION_STRING", "sqlite:///database.db"
)
connect_args = {"check_same_thread": False}

engine = create_engine(database_connection_string, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
