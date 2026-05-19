# Architecture Summary - Corrected

## Folder Structure
- `api/app/` - Contains application source code
  - `main.py` - FastAPI application entry point
  - `models.py` - SQLAlchemy ORM models
  - `schemas.py` - Pydantic schemas for request/response validation
  - `services.py` - Business logic services
  - `config.py` - Configuration management with Pydantic settings
  - `db.py` - Database connection and session management
  - `redis_client.py` - Redis client for caching
  - `celery_app.py` - Celery application for background tasks
  - `tasks.py` - Celery task definitions
- `api/tests/` - Test files
- `api/alembic/` - Database migrations

## Data Models
- `Link` - URL shortening link model
- `ClickEvent` - Click tracking model
- `User` - User model
- `SessionToken` - Session token model

## API Routes
FastAPI routes defined in `main.py`:
- Link management endpoints (create, list, redirect)
- User authentication endpoints
- Analytics endpoints

## Authentication
Uses session-based authentication with session tokens stored in database.

## Database
PostgreSQL database with SQLAlchemy ORM. Connection configured via DATABASE_URL environment variable. Alembic for migrations.

## Additional Infrastructure
- Redis for caching (redis_client.py)
- Celery for background tasks (celery_app.py, tasks.py)
- Pydantic for configuration validation (config.py)
