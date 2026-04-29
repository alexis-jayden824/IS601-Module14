# Module 14 - FastAPI Calculator (BREAD)

This project implements authenticated calculation management with full BREAD operations:
- Browse: `GET /calculations`
- Read: `GET /calculations/{id}`
- Edit: `PUT /calculations/{id}` and `PATCH /calculations/{id}`
- Add: `POST /calculations`
- Delete: `DELETE /calculations/{id}`

Users can register, log in, and manage only their own calculations from the web UI.

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT authentication
- Playwright + Pytest
- Docker / Docker Compose
- GitHub Actions CI/CD

## Local Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
playwright install
```

3. Configure environment variables (example `.env`):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-change-this-in-production
REDIS_URL=redis://localhost:6379/0
```

4. Run the API.

```bash
uvicorn app.main:app --reload
```

Then open:
- App: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

## Testing

Run all tests:

```bash
pytest
```

Run by suite:

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## CI/CD

GitHub Actions workflow:
- Installs dependencies
- Runs unit/integration/e2e tests
- Performs container security scan
- Pushes Docker image on `main`

Docker Hub repository:
- `https://hub.docker.com/r/bowiehikks/601_module9`

## Submission Artifacts Checklist

- GitHub Actions successful run screenshot
- Docker Hub push screenshot
- Front-end BREAD flow screenshots (browse/read/edit/add/delete)
- Reflection document in `docs/reflection.md`
