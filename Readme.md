# Poll Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend).

## Features

- Create and browse questions
- Submit and view answers per question
- Visit tracking: see which questions have been viewed most

## Tech Stack

- **Frontend:** [Svelte](https://svelte.dev/), [Tailwind CSS v4](https://tailwindcss.com/blog/tailwindcss-v4), [shadcn-svelte](https://www.shadcn-svelte.com/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)

---

## Getting Started

Also see:
 - **Frontend:** [Readme](./fe/README.md)
 - **Backend:** [Readme](./be/README.md)

### Backend

```bash
cd be
cp .env.example .env            # optional — defaults work out of the box
uv run fastapi dev              # starts on http://localhost:8000
source .venv/bin/activate       # activates the uv-managed virtualenv if you have another current venv
```

### Frontend

```bash
cd fe
cp .env.example .env        # sets PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev                 # starts on http://localhost:5173
```

---

## Code Review Notes

The following bugs were found in the original submission. They are documented here as feedback for the author.

### Backend

| # | Severity | Description | Location |
|---|----------|-------------|----------|
| B1 | High | Answer-not-found returned `200 OK` instead of `404` | `main.py:85` |
| B2 | High | No CORS middleware — browser requests from `:5173` to `:8000` were blocked | `main.py` (missing) |
| B3 | Medium | No endpoint to fetch answers by question — client had to download all answers and filter in memory | `main.py:71` |
| B4 | Medium | Raw SQLModel table class used as POST request body — callers could supply arbitrary `id` values and overwrite existing records | `main.py:39,63` |
| B5 | Medium | No FK validation on answer creation — an answer could be created for a non-existent question | `main.py:63` |
| B6 | Low | `@app.on_event("startup")` deprecated since FastAPI 0.93 — use a `lifespan` context manager | `main.py:32` |
| B7 | Low | `POST` endpoints returned `200` — resource creation should return `201 Created` | `main.py:39,63` |
| B8 | Medium | No text validation — whitespace-only strings created blank records | `main.py:39,63` |
| B9 | Medium | Routes used singular nouns (`/question/`, `/answer/`) — REST convention is plural | throughout |
| B10 | Low | List query results assigned to singular variable names (`question`, `answer`) — misleading | `main.py:47,72` |

### Frontend

| # | Severity | Description | Location |
|---|----------|-------------|----------|
| F1 | High | `Question` and `Answer` types used but never imported | both `+page.svelte` files |
| F2 | Low | `models.ts` had no `import` or `export` statements, so TypeScript treated it as an ambient script and injected the types into the global namespace. |  `models.ts` |
| F3 | High | Answer POST body sent `question_id` as a string `"5"` instead of number `5` | `answers/+page.svelte:16` |
| F4 | High | Header nav "Answers" link pointed to `/answers` which doesn't exist | `Header.svelte:23` |
| F5 | Medium | `<a>` was a direct child of `<ul>` — invalid HTML; should be wrapped in `<li>` | `questions/+page.svelte:55` |
| F6 | Medium | API base URL hardcoded as `http://localhost:8000` — breaks in any non-local environment | both `+page.svelte` files |
| F7 | Medium | Answers page fetched all answers then filtered client-side — does not scale | `answers/+page.svelte:26` |
| F8 | Medium | Answers page showed no question text — user had no context for what they were answering | `answers/+page.svelte` |
| F9 | Low | `on:submit\|preventDefault` is Svelte 4 legacy event syntax | both `+page.svelte` files |
| F10 | Low | Inconsistent imports: `$app/stores` in one file, `$app/state` (Svelte 5) in another | mixed files |
| F11 | Low | `answer: Answer[]` should be `answers` — misleading singular name for a list | `answers/+page.svelte:6` |
| F12 | Medium | Submit button not disabled during in-flight requests — allowed double-submit | both `+page.svelte` files |
| F13 | Low | Data fetched in `onMount` instead of `+page.ts` load functions — no SSR, slower initial paint | both `+page.svelte` files |
| F14 | High | Reactive refresh with `$: if (refreshTrigger !== prevTrigger)` broke on the second submit; also `$:` reactive statements are legacy in Svelte 5 | both `+page.svelte` files |

---

## What Was Changed

### Phase 1 — Backend restructure, bug fixes, and visits feature

Split `main.py` (all logic in one file) into a proper module structure:

```
be/
├── main.py        # app factory, lifespan, router registration
├── config.py      # pydantic-settings — reads .env; drives CORS/env behaviour
├── middleware.py  # CORSMiddleware: wildcard in dev, FRONTEND_URL in production
├── database.py    # SQLModel engine, SessionDep
├── models.py      # table classes
├── schemas.py     # Create/Read schemas with text validation (no id field)
├── routers/
│   ├── questions.py   # /questions and /questions/{id}/answers routes
│   ├── answers.py     # /answers/{id}
│   └── visits.py      # /visits
└── services/
    ├── questions.py
    ├── answers.py
    └── visits.py
```

**Fixes applied:** B1, B2, B3, B4, B5, B6, B7, B8, B9

**CORS approach:** using `CORSMiddleware` instead of a Vite dev proxy fixes the root cause rather than routing around it, and works in production too.

**Answer route design:** `GET /questions/{id}/answers` and `POST /questions/{id}/answers` (instead of a query-param approach) keeps all question-scoped routes together and is more RESTful.

**Visits Feature:**
- `QuestionVisit` model: `id`, `question_id` (FK), `visited_at` (timestamp)
- `POST /questions/{id}/visit` records a visit
- `GET /visits/` returns questions ordered by visit count (descending)


### Phase 2 — Frontend bug fixes, Svelte 5 modernisation, style overhaul, and visits feature

- Exported types from `models.ts` (F2) and imported them correctly (F1)
- Removed `question_id` from answer POST body — derived from route params server-side (F3)
- Fixed nav links (F4) and `<ul>` structure (F5)
- Replaced hardcoded URL with `PUBLIC_API_URL` from `$env/static/public` and `.env` file (F6)
- Moved data fetching into `+page.ts` load functions; `invalidateAll()` after mutations (F7, F13, F14)
- Show question text on answers page (F8)
- Svelte 5: `onsubmit` handlers (F9), `$app/state` throughout (F10), `$props`/`$derived`/`$state` runes (F9)
- Disabled submit during in-flight requests (F12)

**Visitor Tracking:** 
- Visit recorded in `answers/[id]/+page.ts` load function in parallel with data fetches (no extra round-trip)
- New `/visits` page with visit count badges

**UI overhaul:**
- shadcn-svelte (Button, Card, Badge) with the [qrafthive theme](https://tweakcn.com/themes/cmjgilzlg000404ju2wgs7uj9) — warm orange primary, muted teal secondary
- Tailwind CSS v4 via `@tailwindcss/vite` plugin
- All hardcoded colour classes replaced with design-token classes (`bg-background`, `text-primary`, etc.)
- Dark/light theme toggle via `mode-watcher` — `<ModeWatcher />` mounted in `+layout.svelte` handles FOUC prevention and drives both the toggle icon and the Sonner toast theme from a single reactive source
- Empty states on all pages
- `answers/[id]/+page.ts`: validate `params.id` is a numeric integer before issuing any fetch calls — non-integer paths now return a clean 404 from SvelteKit rather than firing backend requests that would 422

---

## Testing Strategy

Tests were not implemented in scope, but here is what I would add:

### Backend — pytest + httpx

Unit-test service functions in isolation (mock the DB session). Integration-test all routes against a real SQLite in-memory database:

```
tests/
├── test_questions.py   # CRUD, duplicate prevention, text validation
├── test_answers.py     # FK validation, answer creation, 404 on missing question
└── test_visits.py      # visit recording, count aggregation, ordering
```

### Frontend — Playwright

~10 critical-path E2E tests covering:
- Create a question → appears in list
- Navigate to answers page → question text visible, visit recorded
- Submit an answer → appears in list immediately
- Visits page shows correct counts, ordered descending
- Error states: blank input, server error

For API contract testing: use [Prism](https://github.com/stoplightio/prism) to mock the server from the FastAPI OpenAPI schema and run Playwright tests against it — ensures the frontend stays in sync with the API contract without needing a live backend in CI.

---

## What I Would Add With More Time

- **Tests** — see strategy above
- **Real-time updates** — WebSocket or SSE so answers update live as others submit
- **Unique visitor tracking** — session/cookie ID so refreshing doesn't inflate counts
- **Timestamps** — `created_at` on `Question` and `Answer` for sorting and display
- **Delete/edit questions** — basic moderation
- **Duplicate prevention** — reject questions/answers with identical text
- **Docker Compose** — single `docker compose up` to start both services
- **OpenAPI → TypeScript types** — generate frontend types from FastAPI's schema (e.g. `openapi-fetch`) to eliminate the manual `models.ts`
- **Rate limiting** — prevent visit/answer spam
- **API versioning** — prefix routes with `/api/v1`
- **Pagination UI** — backend supports `offset`/`limit` but frontend doesn't use it yet
- **Skeleton Loaders** — more useful once you have production-level data volume and latency
- **Add CSP* — last step to fully prevent XSS in prod. [Svelte Docs: CSP](https://svelte.dev/docs/kit/configuration#csp)
- **Full ADA audit** - shadcn does a decent job but you should always manually test keyboard control, aria labels, contrast, etc.
- **Add docstrings** - add some useful docstrings to the backend code
- **FE validation lib** - would be worth using something like [Zod](https://zod.dev/) for typesafe schema validation if the app grows
- **Add git hooks** - could use [Husky](https://typicode.github.io/husky/) for automatically linting your commit messages, code, and run tests upon committing or pushing.
