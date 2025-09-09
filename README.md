# GoIt PythonWeb HW-08

REST API project using **FastAPI** with **PostgreSQL**.  
Managed with **Poetry** and runnable via **Docker Compose**.

## Features

- Async API using FastAPI
- PostgreSQL database
- Alembic migrations
- Async SQLAlchemy ORM
- User management with CRUD, search, and upcoming birthdays
- Custom error handling

## Requirements

- Python >= 3.11
- Poetry
- Docker & Docker Compose

## Environment Variables

Create a `.env` file with:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
DB_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

RUN -> docker compose up -d --build

## Additional info

    poetry run dev - command to start the API server locally with autoreload for development

    poetry run prod - command to start the API server locally without autoreload
