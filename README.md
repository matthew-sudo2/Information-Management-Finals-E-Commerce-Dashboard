# Sales Management IMS (FastAPI + MySQL)

## Quickstart

1. Create a virtual environment and install backend deps:
	```bash
	cd backend
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt
	```
2. Copy `.env.example` to `.env` and set MySQL credentials and JWT secret.
3. Run the API:
	```bash
	uvicorn app.main:app --reload --port 8000
	```
4. Open `frontend/index.html` in a browser (or serve via `python -m http.server` from `frontend`).

## Notes

- Backend uses FastAPI + SQLAlchemy with MySQL (via PyMySQL driver).
- JWT-based login/register; basic tables: users, customers, products, sales_orders.
- Simple static HTML/JS frontend hitting the API for CRUD.