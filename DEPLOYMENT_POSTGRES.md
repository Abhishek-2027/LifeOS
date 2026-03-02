# PostgreSQL Deployment Guide

This document explains how to configure and deploy the LifeOS backend using PostgreSQL
for production. The repository already includes a Docker Compose file and helper scripts.

## 1. Docker Compose Setup

A `docker-compose.yml` at the project root defines two services:

- **postgres**: runs a PostgreSQL 15 container with named volume `pgdata`.
- **backend**: builds from `backend/Dockerfile` and depends on the postgres service.

To start both services:

```powershell
cd c:\LifeOS
docker-compose up --build -d
```

The backend will be available on `http://localhost:8000` and the database on `localhost:5432`.

By default the compose file uses the following credentials, which you should override
with environment variables or a `.env` file for production:

```
POSTGRES_USER=lifeos
POSTGRES_PASSWORD=lifeospassword
POSTGRES_DB=lifeos
DATABASE_URL=postgresql+asyncpg://lifeos:lifeospassword@postgres/lifeos
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OLLAMA_URL=http://localhost:11434
```

You can supply these variables via a `.env` file placed next to `docker-compose.yml`.

## 2. Initializing the Database

Before running the backend, create the database schema by executing the helper script:

```powershell
cd c:\LifeOS\backend
python init_db.py
```

This will connect using `DATABASE_URL` and run `Base.metadata.create_all()`.

The backend itself also creates tables on startup if they are missing; the script
is just convenient for manual initialization.

## 3. Running the Backend

The backend image starts `uvicorn app.main:app`. You can also run it locally in
venv mode (non-container) with the PostgreSQL URL in `.env`.

Example local `.env` for production:

```
DATABASE_URL=postgresql+asyncpg://lifeos:lifeospassword@localhost/lifeos
SECRET_KEY=supersecretprodkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OLLAMA_URL=http://your-ollama-host:11434
```

When using Docker Compose the environment passed to the container is defined in the
yaml, as shown above. Modify it to point at a managed PostgreSQL instance when
deploying to cloud.

## 4. Migrating from SQLite (Development)

Switching from SQLite is simply a matter of changing `DATABASE_URL` and
reinitializing the schema. Data will **not** be migrated automatically; export
if necessary.

1. Stop the backend and remove `backend/lifeos.db`.
2. Start PostgreSQL and set `DATABASE_URL` appropriately.
3. Run `python init_db.py` or let the backend create tables on startup.

## 5. Adding Alembic (Optional)

For production schema migrations, add Alembic:

```bash
pip install alembic
alembic init backend/alembic
# configure sqlalchemy.url in backend/alembic.ini to read from env
```

Then create and apply revision scripts using standard Alembic commands.

## 6. Deploy to Cloud

When ready to deploy, push the backend Docker image to your registry and run
it along with a PostgreSQL instance. Ensure the `DATABASE_URL` points to the
production database and that proper secrets management is in place.
Add any additional services (e.g. Redis, Celery workers) as required.

## 7. Production Checklist

- [ ] Use a strong, unique `SECRET_KEY` and rotate regularly
- [ ] Enable TLS between clients and the backend (e.g. via reverse proxy)
- [ ] Monitor database connections and scale
- [ ] Backup PostgreSQL data regularly
- [ ] Run `init_db.py` only once or via migration tooling

---

With this documentation and configuration, you're ready to configure PostgreSQL
for a production deployment of the LifeOS backend.
