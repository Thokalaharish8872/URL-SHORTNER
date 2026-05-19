# System Design Module 03: URL Shortener App Foundation

## Artifact: URL Shortener Application

**Implementation Location:** api/app/main.py

**Technology Stack:**
- FastAPI for REST API
- PostgreSQL for data persistence
- Redis for caching
- Celery for background tasks

**Key Features Implemented:**
- POST /shorten - Creates short URL from long URL with custom short code
- GET /{short_code} - Redirects to original URL
- Redis caching for performance (short code lookups cached)
- PostgreSQL database for persistence (URL mappings stored)
- Celery background tasks for cleanup (expired URL cleanup)

**Evidence:**
The application is fully implemented in api/app/main.py with all CRUD operations for URL shortening, including:
- URL shortening with custom short codes
- Redirect functionality with caching
- Database persistence layer
- Background task integration

This artifact serves as the app foundation for System Design Module 03.
