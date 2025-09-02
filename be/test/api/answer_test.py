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


def test_create_answer():
    client.post("/questions", json={"title": "What is your favorite color?"})

    response = client.post("/questions/1/answers", json={"text": "Yellow"})

    if response.status_code != 200:
        print(response.text)

    assert response.status_code == 200
    assert response.json() == {"id": 1}


def test_list_answers_for_question():
    client.post("/questions", json={"title": "What is your favorite color?"})

    response = client.get("/questions/1/answers", params={"offset": 0, "limit": 10})
    if response.status_code != 200:
        print(response.text)

    assert response.status_code == 200
    assert len(response.json()) == 0

    client.post("/questions/1/answers", json={"text": "Yellow"})

    response = client.get("/questions/1/answers", params={"offset": 0, "limit": 10})

    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [{"id": 1, "text": "Yellow"}]


def test_list_answers():
    client.post("/questions", json={"title": "What is your favorite color?"})

    response = client.get("/questions/1/answers", params={"offset": 0, "limit": 10})
    if response.status_code != 200:
        print(response.text)

    assert response.status_code == 200
    assert len(response.json()) == 0

    client.post("/questions/1/answers", json={"text": "Yellow"})

    response = client.get("/answers", params={"offset": 0, "limit": 10})

    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [{"id": 1, "text": "Yellow"}]

