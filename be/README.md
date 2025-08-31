# Running a FastAPI Project with `uv`

[uv](https://github.com/astral-sh/uv) is a fast Python package manager and runner. To run a FastAPI project using `uv`, follow these steps after installing uv:

```bash
    uv run fastapi run
    source .venv/bin/activate
```

# Feedback

* Structure
  * Although current size of project allows all in one file, splitting code into multiple files
    * Models
    * Routes
* DB
  * SQLite the right DB? -> Maybe use PostgreSQL or MySQL (via docker)
  * Separate initialization of DB into separate process
  * Maybe use seed data for local development (to have testing data in local development)
  * You might want to have migrations for DB schema changes
* Server
  * CORS are not allowed from FE -> leads to 307 for any FE request
* Models
  * In the future for more complex functionality you might want to have different models for API and DB (`Pydantic` offers data validation, `SQLAlchemy` offers ORM, which are unified in SQLModel right now)
* API
  * POST Question
    * Accepts empty "text" -> add validation
    * API accepts `question.id` field, which leads to a DB duplicate key constraint error -> make `question.id` not sendable OR handle DB failure gracefully with e.g. 409 Conflict
  * GET Answers
    * On not found it returns 200 -> should return a 404 Not Found response
