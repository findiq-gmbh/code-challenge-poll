# Poll Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend).

## Features

- Create and manage Questions
- See Answers to Questions

## Tech Stack

- **Frontend:** [Svelte](https://svelte.dev/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)


## Run & Develop

See:
 - **Frontend:** [Readme](./fe/README.md)
 - **Backend:** [Readme](./be/README.md)

# Feedback Backend

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

# Feedback Frontend

* All dependencies are defined as `devDependencies` -> should be split into `dependencies` (actually used for PROD runtime) and `devDependencies`
* Following versions of packages have vulnerabilities
  * `@eslint/plugin-kit <0.3.4` LOW
  * `cookie <0.7.0` LOW
  * `devalue <5.3.2` HIGH
* UX/UI
  * Home is an unused page, that either should have content or be removed
  * The answer page is not showing the question it refers to
  * Question page is not showing an info, when no questions are available so far
  * Questions API accepts `limit=100` as max, but the FE is not providing a pagination, means if there are more than 100 answers, the user will not be able to see them all
  * Answer page is not showing an info, when no answers are available so far
  * Answers are not reloaded after submitting an answer
  * Submitting an answer does not show the user any feedback and since it's not reloading he might think his answer was lost and sends it again.
  * Answers API accepts `limit=100` as max, but the FE is not providing a pagination, means if there are more than 100 answers, the user will not be able to see them all
