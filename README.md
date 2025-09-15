## EHR Lab Order System

Production site: https://ehr-lab-order-system-jsmans568-mistirs-projects.vercel.app/login

**What It Is**

An end‑to‑end, hospital‑grade EHR and Lab Orders platform:
- Append‑only clinical charting (encounters/notes, problems, allergies, medications)
- Lab orders lifecycle with role‑based transitions (Physician/Nurse/LabTech)
- Labs results CRUD by internal lab users and automatic surfacing in the chart
- JWT authentication with simple, env‑driven users (no user DB)
- Modular monolith (Flask API + Vite/React UI) backed by Postgres

**Tech Stack**
- Backend: Flask 3, Flask‑SQLAlchemy 3, Flask‑JWT‑Extended, Alembic, Gunicorn
- DB: PostgreSQL (local via Docker, prod via Neon)
- Frontend: React + Vite, Tailwind CSS v4
- Infra: Docker Compose (local), Render (API), Vercel (UI)

**Repo Structure**
- `backend/`
  - `app/`
    - `__init__.py` (app factory, CORS, JWT, blueprints)
    - `auth/` (login routes; AUTH_USERS parsing → JWT with roles + lab)
    - `modules/`
      - `patient/` (patient domain + ORM)
      - `ehr/` (encounters, notes, problems, allergies, medications ORM)
      - `orders/` (orders ORM incl. `lab_code`)
      - `labs/` (lab results ORM)
    - `routes.py` (core REST endpoints)
  - `migrations/` (Alembic; 0001..0007)
  - `requirements.txt`, `Dockerfile`, `start.sh`
- `frontend/`
  - `src/pages/` (Login, Patients, PatientDetail, OrderDetail, Labs)
  - `src/components/` (NavBar)
  - `src/lib/` (`api.js`, `auth.js`)
  - `vite.config.js`, `postcss.config.js`, `vercel.json`

**Modules Overview**
- Patient: create/search/list; demographics + MRN; latest encounter type for list view
- EHR: encounters (OUT/ER/IN), append‑only notes, problems/allergies/meds
- Orders: lab orders linked to encounters; `lab_code` assigns ownership to a lab
- Labs: results linked to orders; LabTech can create/update/delete results

**RBAC (JWT roles)**
- Physician: full charting; place orders; status collected; approve correction
- Nurse: full charting; view orders; can move ordered→collected if used
- LabTech: see only their lab’s orders; status collected→in_progress→resulted→corrected; full CRUD results

**Local Development**

Prereqs: Docker Desktop, Node 20+ (for Vite 7), Python 3.11+

1) Copy env and start services
- `cp .env.example .env`
- `docker compose up --build`
- UI: http://localhost:5173
- API health: http://localhost:5001/health

2) Dev without Docker (optional)
- Frontend: `cd frontend && npm install && npm run dev`
- Backend (SQLite dev):
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r backend/requirements.txt`
  - `cd backend && USE_SQLITE=1 FLASK_APP=app:create_app flask run`

3) Database & migrations
- Alembic runs automatically on backend start (local and Render)
- Migrations add schemas (`patient`, `ehr`, `orders`, `labs`) and tables

**Environment Variables (API)**
- `DATABASE_URL` Postgres SQLAlchemy URL (e.g., Neon; include `sslmode=require`)
- `JWT_SECRET` secret for JWT signing
- `AUTH_USERS` comma‑separated users: `username:password:Role[:LABCODE]`
  - Role accepts: Physician|Nurse|LabTech (case‑insensitive aliases allowed)
  - For LabTech, LABCODE optional → falls back to `DEFAULT_LAB_CODE`
- `DEFAULT_LAB_CODE` default lab assignment for orders and LabTech claims (e.g., `LAB`)

**Deployment**
- Backend: Render (Docker). Ensure env set: `DATABASE_URL`, `JWT_SECRET`, `AUTH_USERS`, `DEFAULT_LAB_CODE`.
- Frontend: Vercel (Root: `frontend`, Build: `npm install && npm run build`, Output: `dist`).
- CORS: API allows all origins out of the box (can be restricted later).

**User Manual (PoC)**

- Sign in
  - Doctor: `doctor / doctor12`
  - Nurse: `nurse / nurse12`
  - LabTech: `labtech / labtech12`

- Physician/Nurse (after login)
  - Top bar shows “Patients”. Click to see the table.
  - “Add Patient” toggles a create form (Physician/Nurse only).
  - Open a patient → Start encounter (OUT/ER/IN) → Append note.
  - Physician only: Place lab order (tests comma‑separated). New orders default to “collected”.
  - Order page: shows status and results; status transitions restricted by role.

- LabTech (after login)
  - Top bar shows “Orders”; page lists only your lab’s orders.
  - Open an order → advance status collected→in_progress→resulted→corrected.
  - Add lab results inline; edit or delete them; changes show immediately.

**API Highlights**
- Patients: `POST /api/patients`, `GET /api/patients`, `GET /api/patients/search?q=`, `GET /api/patients/{id}/summary`, `GET /api/patients/{id}/orders`
- Encounters/Notes: `POST /api/encounters`, `POST /api/ehr/notes`
- Orders: `POST /api/orders/lab` (Physician), `GET /api/orders/lab/{id}`, `PATCH /api/orders/lab/{id}/status`
- Labs: `GET /api/labs/orders` (LabTech), `POST /api/orders/lab/{id}/results`, `PATCH`/`DELETE` per result

**Extensibility**
- Add new modules under `backend/app/modules/*` with their ORMs and blueprints.
- Introduce code systems (ICD‑10, RxNorm, LOINC) as reference tables.
- Add audit trails, soft‑deletes for corrections, and version history tables.
- Replace AUTH_USERS with a user DB and password hashing (Flask‑Security or custom).
- Add pagination and filters to list endpoints; add search refinements.

**Notes**
- Tailwind CSS v4 is enabled via `@import "tailwindcss";` (no config required).
- Vite dev server binds `0.0.0.0` in Docker for easy access.
- Backend defaults to Postgres; set `USE_SQLITE=1` for local SQLite dev.
