# Polling Application - Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend).

## 🚀 Features

- Create questions
- Submit answers to specific questions
- View all answers for a question

## 🛠️ Tech Stack

**Frontend:**

- **SvelteKit** [https://kit.svelte.dev](https://kit.svelte.dev)
- **TypeScript** [https://www.typescriptlang.org](https://www.typescriptlang.org)
- **Vite** [https://vitejs.dev](https://vitejs.dev)

**Backend:**

- **FastAPI** [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **SQLModel (SQLite)** [https://sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- **SQLite** [https://www.sqlite.org](https://www.sqlite.org)

**Dev Tools:**

- **Vite Proxy** [https://vitejs.dev/config/server-options.html#server-proxy](https://vitejs.dev/config/server-options.html#server-proxy)
- **uv / uvicorn** [https://www.uvicorn.org](https://www.uvicorn.org)
- **npm** [https://www.npmjs.com](https://www.npmjs.com)

## 📦 Setup & Running Locally

See:

- **Frontend:** [Readme](./fe/README.md)
- **Backend:** [Readme](./be/README.md)

## 🔮 Future Improvements

### Backend

- Introduce backend route for `GET /question/{id}/answers` (avoids filtering client-side).
- Introduce routers/modules for better structure (`questions`, `answers`, `stats`).
- Add schemas for validation and explicit typing.
- Build proper database migrations.
- Add efficient endpoint for fetching answers for a specific question.
- Add authentication/authorization layer (admin interface visits is public).

### Frontend

- Create small API client wrapper for fetch calls.
- Global error-handling strategy, add reusable components for errors, loading states, and forms.
- Apply a scale-based spacing and typography system for visual consistency.
- Improve responsive layout behavior.
- Consider complying with A11y standards.

### Testing

- Add FastAPI tests for new endpoints.
- Add Vitest component tests for question/answer flows.
- Include linting & formatting checks in CI.
