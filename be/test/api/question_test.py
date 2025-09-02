from fastapi.testclient import TestClient

import sys
import os

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from enums import AppEnvironmentEnum, EnvironmentNameEnum

os.environ[EnvironmentNameEnum.APP_ENVIRONMENT.value] = AppEnvironmentEnum.TESTING.value

from main import app, create_db_and_tables

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    create_db_and_tables()
    yield


def test_create_question():
    response = client.post("/questions", json={"title": "What is your favorite color?"})
    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert response.json() == {"id": 1}


def test_list_questions():
    response = client.get("/questions", params={"offset": 0, "limit": 10})
    if response.status_code != 200:
        print(response.text)

    assert response.status_code == 200
    assert len(response.json()) == 0

    client.post("/questions", json={"title": "What is your favorite color?"})

    response = client.get("/questions", params={"offset": 0, "limit": 10})

    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [
        {"id": 1, "title": "What is your favorite color?", "visitor_count": 0}
    ]
