# Poll Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend). Users can create questions, submit answers, and view analytics.


## Features

- Create and manage Questions
- Submit Answers to Questions  
- Track question visit analytics
- RESTful API design
- Docker containerization


## Tech Stack

- **Frontend:** [Svelte](https://svelte.dev/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** SQLite
- **Containerization:** Docker & Docker Compose


## Architecture

### Backend (`be/`)
- **FastAPI** with **SQLModel** for the REST API
- SQLite database with models: `Question`, `Answer` and `QuestionVisit`
- Single-file architecture in `main.py`
- Database auto-creation on startup

### Frontend (`fe/`)
- **Svelte** with TypeScript
- Route structure:
  - `/` - Home page
  - `/questions` - Create and view questions
  - `/question/[id]/answers` - View and create answers for specific questions
  - `/questions/visits` - View question visit analytics
- Shared TypeScript interfaces in `routes/models.ts`
- Configurable backend URL (defaults to `http://localhost:8000`)


## Docker Setup

### Quick Start

1. **Clone and navigate to the project:**
   ```bash
   git clone git@github.com:mostafa-kenawey/code-challenge-poll.git
   cd code-challenge-poll
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Frontend:** http://localhost:3000
   - **Backend API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs

### Docker Commands

- **Start services in background:**
  ```bash
  docker-compose up -d --build
  ```

- **View logs:**
  ```bash
  docker-compose logs -f
  ```

- **Stop services:**
  ```bash
  docker-compose down
  ```

- **Rebuild and restart:**
  ```bash
  docker-compose down
  docker-compose up --build
  ```


## Local Development Setup

### Backend Development
See: [Backend README](./be/README.md)

### Frontend Development  
See: [Frontend README](./fe/README.md)


## Code Review and Feedback

### Backend Review

1. **Wrong HTTP Status Code** 
    - Returns status 200 instead of 404 for missing answers

2. **Inconsistent Variable Naming**
    - Variables `question` and `answer` should be plural when containing lists, Confusing single/plural naming convention

3. **Dependency Injection**
    - Direct database operations in route handlers, Use service layer pattern instead direct database operations

4. **Missing Validation**
    - No validation for question_id in Answer creation, Could create orphaned answers referencing non-existent questions

5. **Database Best Practices**
    - **Migrations**: Apply database migrations, configure proper pool settings and add strategic indexes for performance

6. **Missing CORS Configuration**
    - Frontend runs on different port but no CORS setup

7. **Inefficient Answer Filtering**
    - No endpoint to get answers by question_id, Frontend fetches all answers and filters client-side

8. **Missing Error Handling**
    - No specific error handling for database operations, Generic error messages not helpful for debugging

9. **Pagination**
    - Implement pagination controls questions and answers with and page number navigation

10. **Missing Tests**
    - Tests are not implemented. Tests are needed for API validation, database operations and error handling tests pending

### Frontend Review

1. **Type Declaration Missing** 
    - `Question` and `Answer` types used but not imported, Should import from `./models.ts`

2. **Hardcoded Backend URL**
    - `http://localhost:8000` hardcoded in multiple places, Should use environment variables or configuration

3. **Poor Error Handling**
    - Generic error messages not user-friendly, No specific handling for different error types

4. **Inefficient Data Fetching**
    - Answer page fetches ALL answers then filters, Should have dedicated API endpoint

5. **Missing Reactive Declaration**
    - Questions page uses string comparison for reactive updates, Could use more reliable reactive patterns

6. **No Form Validation**
    - Only basic HTML5 required validation, No client-side validation feedback

7. **Missing Navigation Feedback**
    - No breadcrumbs or clear navigation context, Users can't easily understand current location

8. **No Loading States for Submissions**
    - Forms don't show loading state during submission, Users might submit multiple times

9. **Pagination**
    - Implement pagination controls questions and answers with next/previous buttons and page number navigation

10. **Missing Tests**
    - This is a known gap in the current implementation. Component rendering and user interaction tests required


### Architecture Issues

1. **Missing Indexes**
   - No proper indexing strategy for foreign keys, Performance issues as data grows

2. **No Timestamps**
   - No created_at/updated_at fields, Cannot track when questions/answers were created

3. **No Rate Limiting**
   - No protection against spam submissions

4. **No Caching Strategy**
   - Every request hits database


## My Changes: Backend and Frontend Changes and Bug Fixes

### 01 - Fix Cross-Origin Resource Sharing Issue
- Added CORS middleware configuration to allow frontend-backend communication
- Configured proper CORS origins, methods, and headers

### 02 - Fix Answer Show Endpoint and Error Handling
- Fixed answer show endpoint responding with 404 instead of 200
- Added question existence validation in backend for answer endpoints
- Implemented proper error handling for:
  - Empty question text (BE/FE)
  - Duplicate question text validation
  - Empty answer text (BE/FE) for each question
  - Duplicate answer text validation for each question
  - Better frontend error handling for answers

### 03 - Database Schema Improvements
- Added `Question.created_at` and `Answer.created_at` timestamps
- Removed generic `/answer` endpoint, replaced with `/question/{id}/answers`
- Followed REST API best practices for endpoints (`/questions`, `/answers`)
- Added proper question list return in questions endpoint
- Changed frontend route from `/answers/1` to `/question/1/answers`

### 04 - Question Visit Analytics
- Added visit tracking functionality
- Created `QuestionVisit` model for storing visit data
- Implemented visit logging when accessing question answer pages
- Added analytics page showing visit counts per question

### 05 - Database Conventions
- Implemented proper table naming conventions
- Added proper foreign key relationships
- Improved database schema structure

### 06 - UI/UX Improvements
- Added page showing visit statistics for each question
- Implemented proper "not found" question handling
- Improved styling, UI, and UX flow
- Better navigation and user feedback

### 07 - Docker Implementation
- Created comprehensive Docker setup
- Added Docker Compose configuration
- Multi-stage builds for optimized containers
- Production-ready containerization


## TODO

### Future Improvements

- Add comprehensive test coverage
- Add API versioning and authentication
- Add environment variables configuration (DB config, ..)
- Add model validation for uniqueness, presence and error handling
- Implement pagination, caching strategy and rate limiting
- Handle text input validation (trim spaces from start/end)
- Implement min/max length validation for questions and answers
- Add structured logging
- Disable form submissions while submitting

### Architecture Improvements

Adopt Multi-File Structure instead of single `main.py` file

**Recommended**:
```
be/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── database.py
│   └── config.py
```