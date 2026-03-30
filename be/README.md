# Backend

FastAPI + SQLModel + SQLite, managed with [uv](https://github.com/astral-sh/uv).

## Running

```bash
cp .env.example .env          # optional — defaults work out of the box
uv run fastapi dev            # development server with auto-reload on http://localhost:8000
source .venv/bin/activate     # activates the uv-managed virtualenv if you have a different venv currently loaded
```

## Environment variables

See `.env.example`. All variables have sensible defaults so the app runs without a `.env` file in development.

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Set to `production` to restrict CORS to `FRONTEND_URL` |
| `DATABASE_URL` | `sqlite:///database.db` | SQLAlchemy connection string |
| `FRONTEND_URL` | `http://localhost:5173` | Allowed origin in production CORS |
