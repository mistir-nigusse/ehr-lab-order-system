# ehr-lab-order-system

Getting Started
- Prereqs: Docker Desktop, Node 18+ (optional for local build), Python 3.11+ (optional for local run)
- Copy env: `cp .env.example .env`

Run with Docker
- Start: `docker compose up --build`
- Frontend: http://localhost:5173
- Backend: http://localhost:5001/health
- DB: Postgres on port 5432

Local Dev (without Docker)
- Frontend: `cd frontend && npm install && npm run dev`
- Backend (SQLite dev mode):
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r backend/requirements.txt`
  - `cd backend && USE_SQLITE=1 FLASK_APP=app:create_app flask run`

Notes
- Tailwind CSS v4 is enabled via `@import "tailwindcss";` in `frontend/src/index.css`.
- Vite dev server is configured to bind `0.0.0.0` for Docker.
- Backend supports Postgres (default) and falls back to SQLite when `USE_SQLITE=1`.
