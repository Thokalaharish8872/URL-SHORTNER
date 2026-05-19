# System-Level Context Document

## Architecture Summary

**Framework**: Python FastAPI
- Version: Latest stable (check api/requirements.txt)
- Async support enabled

**Project Organization**:
- `api/app/` - Main application directory
  - `main.py` - FastAPI application entry point and route registration
  - `models.py` - SQLAlchemy ORM models
  - `schemas.py` - Pydantic schemas for request/response validation
  - `services.py` - Business logic services
  - `config.py` - Configuration management using Pydantic settings
  - `db.py` - Database connection and session management
  - `redis_client.py` - Redis client for caching
  - `celery_app.py` - Celery application for background tasks
  - `tasks.py` - Celery task definitions
- `api/tests/` - Test files
- `api/alembic/` - Database migrations
  - `versions/` - Migration files

**ORM/Database**:
- SQLAlchemy ORM
- PostgreSQL database
- Alembic for migrations
- Connection string via DATABASE_URL environment variable

**Route Registration**:
- Routes are registered in `api/app/main.py` using FastAPI decorators
- Pattern: `@app.get("/path")`, `@app.post("/path")`, etc.
- Dependency injection for database session: `Depends(get_db)`

**Middleware**:
- FastAPI middleware registered in `api/app/main.py`
- CORS middleware configured
- Error handling middleware

## Coding Conventions

**Naming**:
- Classes: PascalCase (e.g., `User`, `Link`)
- Functions and variables: snake_case (e.g., `get_user`, `user_id`)
- Database tables: snake_case, plural (e.g., `users`, `links`)
- Pydantic schemas: PascalCase with "Create", "Response", "Update" suffixes (e.g., `UserCreate`, `UserResponse`)

**File Naming**:
- Python files: snake_case with .py extension (e.g., `models.py`, `services.py`)
- Migration files: timestamped description (e.g., `001_create_users.py`)
- Test files: test_*.py pattern

**Error Handling**:
Error responses follow this format:
```json
{
  "detail": "Error message here"
}
```

Status codes:
- 400 for validation errors
- 401 for missing authentication
- 403 for insufficient permissions
- 404 for missing resources
- 422 for validation errors (Pydantic validation)
- 500 for unexpected errors

IMPORTANT: All error responses MUST use FastAPI's HTTPException with the `detail` parameter.
Do NOT use custom error object shapes unless documented.
Do NOT use plain text error messages without JSON structure.
Do NOT return error responses with fields like "status", "statusCode", or "code" - only use "detail".

Example usage from existing code:
```python
from fastapi import HTTPException

# For not found
raise HTTPException(status_code=404, detail="Link not found")

# For validation errors
raise HTTPException(status_code=422, detail="Team name is required")
```

**Validation**:
- Pydantic schemas for request/response validation
- Field constraints in Pydantic models (e.g., `max_length`, `regex`)
- Database constraints in SQLAlchemy models (e.g., `nullable`, `unique`)
- Automatic validation via FastAPI integration with Pydantic

**Authentication**:
- Session-based authentication using session tokens
- Session tokens stored in database
- Protected routes use dependency injection: `Depends(get_current_user)`
- User must be authenticated to access protected endpoints
- No JWT or OAuth currently implemented

## Constraints

**Dependencies**:
- No new pip dependencies without explicit justification
- Must use existing libraries: FastAPI, SQLAlchemy, Pydantic, Celery, Redis
- Check `api/requirements.txt` for available packages

**Authentication**:
- Must use existing session-based authentication
- Do NOT create new auth middleware or authentication logic
- Protected routes must use `Depends(get_current_user)` dependency
- Session tokens must be stored in database (see existing implementation)

**Error Responses**:
- Must follow existing error format: `{"detail": "message"}`
- Use appropriate HTTP status codes
- Do NOT invent new error response formats

**File Conventions**:
- New models go in `api/app/models.py`
- New schemas go in `api/app/schemas.py`
- New services go in `api/app/services.py`
- New routes go in `api/app/main.py`
- New migrations go in `api/alembic/versions/`

**Database Changes**:
- All database schema changes MUST include Alembic migrations
- Migration files must follow existing naming pattern
- Run migrations with `alembic upgrade head`
- Do NOT modify database directly without migration

**Background Tasks**:
- Use Celery for background tasks
- Define tasks in `api/app/tasks.py`
- Configure Celery in `api/app/celery_app.py`
- Use Redis as Celery broker

**Testing**:
- Test files in `api/tests/`
- Use pytest framework
- Follow existing test patterns in `api/tests/`
