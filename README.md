# Voice Translator API

## Run with Docker Compose

From this directory (`apps/server`), build and start the API and PostgreSQL:

```powershell
docker compose up --build -d
```

Apply database migrations:

```powershell
docker compose exec api alembic upgrade head
```

The API is available at:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

Useful Docker Compose commands:

```powershell
docker compose logs -f api       # Follow API logs
docker compose logs -f db        # Follow PostgreSQL logs
docker compose ps                # Show service status
docker compose down              # Stop and remove containers
docker compose up --build -d     # Rebuild and start after code/image changes
```

## Run locally with PowerShell

Run these commands from `apps/server`. Start PostgreSQL:

```powershell
docker compose up -d db
```

Create and activate the virtual environment, then install dependencies (skip creation if `venv` already exists):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in this directory with the local database URL and a JWT secret:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db
JWT_SECRET=replace-with-a-long-random-secret
```

Apply database migrations, then run the development server:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; its health check is `http://127.0.0.1:8000/health`.

## Database migrations

After changing SQLAlchemy models, create a migration:

```powershell
alembic revision --autogenerate -m "describe the schema change"
```

Review the generated migration under `alembic/versions/`, then apply it:

```powershell
alembic upgrade head
```

To check the current migration revision:

```powershell
alembic current
```

Do not run `alembic init` again; this project already has an Alembic environment.

docker compose up -d db
alembic upgrade head


```
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
