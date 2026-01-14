# Project Structure Guide

## High-level layout

```
Information-Management-Finals-E-Commerce-Dashboard/
├─ backend/                # FastAPI + SQLAlchemy app
│  ├─ app/
│  │  ├─ core/             # Security helpers (hashing, JWT)
│  │  ├─ models/           # SQLAlchemy models (tables)
│  │  ├─ routers/          # API route modules (auth, sales CRUD)
│  │  ├─ config.py         # Settings loader (env-driven)
│  │  ├─ database.py       # Engine/session/Base setup
│  │  ├─ main.py           # FastAPI app factory + router mount
│  │  └─ schemas.py        # Pydantic schemas (request/response)
│  └─ requirements.txt     # Backend dependencies
├─ frontend/               # Static UI (HTML/CSS/JS)
│  ├─ assets/              # Frontend scripts and styles
│  └─ index.html           # Entry page hitting FastAPI endpoints
├─ docs/                   # Documentation and deliverables
│  └─ STRUCTURE.md         # This file
├─ .env.example            # Sample env vars (copy to .env)
├─ README.md               # Quickstart and stack overview
├─ LICENSE                 # MIT license
└─ .gitignore              # Ignore rules
```

## Backend (FastAPI)
- `backend/app/main.py`: Creates the FastAPI app, configures CORS, mounts static frontend, and registers routers. Also triggers `Base.metadata.create_all` for quick DB setup during development.
- `backend/app/config.py`: Centralized settings using `pydantic-settings`. Reads `.env` for MySQL URL, JWT secret, CORS origins, and app metadata.
- `backend/app/database.py`: Builds the SQLAlchemy engine/session factory against MySQL via the `DATABASE_URL`; exposes `get_db` dependency and declarative `Base`.
- `backend/app/core/`: Security utilities.
  - `security.py`: Password hashing/verification with `passlib` and JWT creation with `python-jose`.
- `backend/app/models/`: Database tables (aligned to the ERD requirement of 3–5 related tables).
  - `models.py`: Defines `User`, `Customer`, `Product`, and `SalesOrder` with primary/foreign keys and relationships.
- `backend/app/schemas.py`: Pydantic models for inputs/outputs (users, customers, products, orders, tokens) to validate requests and shape responses.
- `backend/app/routers/`: API route modules grouped by concern.
  - `auth.py`: Register/login, JWT issuance, and `get_current_user` dependency for protected routes.
  - `sales.py`: CRUD endpoints for customers, products, and sales orders (create/read/update/delete).
- `backend/requirements.txt`: Locked list of backend libs (FastAPI, SQLAlchemy, PyMySQL, auth helpers, multipart uploads).

## Frontend (HTML/CSS/JS)
- `frontend/index.html`: Minimal UI to call backend endpoints—login plus simple forms for customers/products/orders and a table for recent orders.
- `frontend/assets/styles.css`: Styling theme (dark, accent), layout grid, and table styles.
- `frontend/assets/app.js`: Fetch helpers and event handlers for login and CRUD actions; uses bearer token from login to call protected routes.

## Environment & Ops
- `.env.example`: Template for app env vars (MySQL credentials/URL, JWT secret, CORS origins, app port). Copy to `.env` before running.
- `README.md`: Quickstart steps (create venv, install deps, run `uvicorn`, open frontend), stack notes, and pointers.
- `.gitignore`: Standard Python ignores (venv, caches, build artifacts, IDE files).
- `LICENSE`: MIT license for the project.

## How this satisfies criteria
- **Database design**: Models define 4 related tables with primary keys, foreign keys, and relationships (users ↔ sales_orders; customers/products ↔ sales_orders).
- **CRUD**: `sales.py` exposes create/read/update/delete for customers, products, and orders; `auth.py` covers user creation via register.
- **Tools**: Python + FastAPI + SQLAlchemy with MySQL backend; static HTML/CSS/JS frontend.
- **UI**: Simple forms and table to trigger real CRUD operations via HTTP calls to the API.
- **Docs/Presentation**: This file plus README give structure context; extend `docs/` with the required 7–8 page write-up and screenshots for the final deliverable.
