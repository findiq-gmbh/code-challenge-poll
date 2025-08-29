# Backend - FastAPI Application

FastAPI backend with SQLite database.

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager


## Quick Start with uv

Navigate to the backend directory
```bash
    cd be
```

Install dependencies and run the server
```bash
    uv run fastapi run
```

### Access the application:**
   - **API Server:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs
   - **Alternative Docs:** http://localhost:8000/redoc

## API Endpoints

### Questions
- `GET /questions/` - List all questions with pagination
- `POST /questions/` - Create a new question
- `GET /question/{id}` - Get specific question by ID
- `GET /question/{id}/answers` - Get all answers for a specific question
- `POST /question/{id}/visit` - Track a visit to question's answer page
- `GET /questions/visits` - Get visit analytics for all questions

### Answers
- `POST /answers/` - Create a new answer for a question

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation
- `GET /openapi.json` - OpenAPI specification