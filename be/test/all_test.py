from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

# To collect all tests here, does not make sense ofc. but for time reasons, i put it here


def test_list_questions():
    response = client.get("/questions")
    assert response.status_code == 200
    assert response.json() == []


def test_create_question():
    response = client.post(
        "/questions", json={"question": "What is your favorite color?"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1}


# todo: add all other tests here
