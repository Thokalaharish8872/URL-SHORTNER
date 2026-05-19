# Project Documentation: Upsk Bootcamp Projects

## Overview

This documentation covers all projects completed through the Upsk Bootcamp skills. The primary application is a **URL Shortener Service** built as part of the System Design Fundamentals skill, with additional planning and documentation work from Technical Communication and Decomposition & Execution Planning skills.

---

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async-compatible with future=True)
- **Migration Tool**: Alembic
- **Caching**: Redis
- **Background Jobs**: Celery with Redis broker
- **Authentication**: JWT (stateful with database token storage)
- **Password Hashing**: bcrypt

### Frontend
- None (API-only service)

### Infrastructure
- **Python**: 3.x
- **Environment Configuration**: Pydantic Settings with .env files
- **Logging**: Python logging with structured error handling

---

## Architecture

### System Components

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────────────┐
│         FastAPI Application         │
│  (api/app/main.py)                  │
│  - Authentication middleware        │
│  - Rate limiting middleware         │
│  - Exception handling middleware     │
└──────┬──────────────────────────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌────────────┐
│ PostgreSQL   │ │  Redis   │ │   Celery   │
│ (Primary DB) │ │ (Cache)  │ │ (Workers)  │
└──────────────┘ └──────────┘ └────────────┘
```

### Directory Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & endpoints
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── services.py          # Business logic (AuthService, LinkService)
│   ├── db.py                # Database connection & session management
│   ├── config.py            # Configuration & environment variables
│   ├── redis_client.py      # Redis client with graceful degradation
│   ├── celery_app.py        # Celery configuration
│   └── tasks.py             # Background tasks (click logging, cleanup)
├── alembic/                 # Database migrations
│   └── versions/
├── scripts/                 # Utility scripts
└── tests/                   # Test files

artifacts/                   # Upsk skill artifacts
├── adaptation/             # Module 7 adaptation artifacts
├── dependencies/           # Module 2 dependency graphs
├── integration/            # Module 8 integration plans
└── requirements/           # Module 1 requirements extraction

progress/                    # Upsk progress tracking
├── decomposition-execution-planning/
├── evidence/
├── system-design/
└── technical-communication/
```

---

## Database Schema

### Tables

#### 1. `links` - URL shortening records
| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-incrementing primary key |
| code | string (64, unique) | Short code for URL |
| long_url | text | Original long URL |
| created_at | datetime (timezone) | Creation timestamp |
| created_by | string (255, indexed) | User who created the link |
| expires_at | datetime (timezone, nullable) | Optional expiration date |
| tags | array(string, nullable) | Tags for organization |
| search_vector | tsvector | Full-text search index (PostgreSQL) |

#### 2. `click_events` - Analytics data
| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-incrementing primary key |
| link_id | int (FK) | Reference to links.id |
| clicked_at | datetime (timezone) | Click timestamp |
| user_agent | string (512, nullable) | Browser user agent |
| referrer | string (512, nullable) | HTTP referrer |
| ip_hash | string (255) | Hashed IP address for privacy |

**Index**: Composite index on (link_id, clicked_at) for analytics queries

#### 3. `users` - User accounts
| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-incrementing primary key |
| email | string (255, unique, indexed) | User email |
| hashed_password | string (255) | bcrypt hashed password |
| created_at | datetime (timezone) | Account creation timestamp |

#### 4. `session_tokens` - JWT session management
| Column | Type | Description |
|--------|------|-------------|
| id | int (PK) | Auto-incrementing primary key |
| token | string (255, unique, indexed) | JWT token |
| user_id | int (FK) | Reference to users.id |
| created_at | datetime (timezone) | Token creation timestamp |
| expires_at | datetime (timezone) | Token expiration timestamp |

---

## API Endpoints

### Authentication

#### POST `/register`
- **Purpose**: Create new user account
- **Request**: `{ email: string, password: string }`
- **Response**: `{ id: int, email: string, created_at: datetime }`
- **Error**: 400 if email already exists

#### POST `/login`
- **Purpose**: Authenticate user and receive JWT token
- **Request**: OAuth2PasswordRequestForm (username=email, password)
- **Response**: `{ access_token: string, token_type: "bearer" }`
- **Error**: 401 if credentials invalid

#### POST `/logout`
- **Purpose**: Invalidate current session token
- **Request**: Bearer token in Authorization header
- **Response**: `{ message: "Successfully logged out" }`

### URL Shortening

#### POST `/links`
- **Purpose**: Create shortened URL
- **Auth**: Required (Bearer token)
- **Request**: 
  ```json
  {
    "long_url": "https://example.com/very/long/url",
    "custom_code": "mylink" (optional),
    "expires_at": "2025-12-31T23:59:59Z" (optional),
    "tags": ["marketing", "campaign"] (optional)
  }
  ```
- **Response**: Link object with id, code, long_url, created_at, created_by
- **Error**: 400 if custom code already exists

#### GET `/links`
- **Purpose**: List user's links
- **Auth**: Required (Bearer token)
- **Query**: `skip=0`, `limit=100`
- **Response**: Array of Link objects

#### GET `/links/search`
- **Purpose**: Search links by code, URL, or tags
- **Auth**: Required (Bearer token)
- **Query**: `q=search_term`, `skip=0`, `limit=100`
- **Implementation**: PostgreSQL full-text search with ILIKE fallback
- **Response**: Array of matching Link objects

#### GET `/{code}`
- **Purpose**: Redirect to original URL
- **Rate Limit**: 10 requests per 60 seconds per code
- **Flow**:
  1. Check rate limit in Redis
  2. Fetch link from cache (Redis) or database (PostgreSQL)
  3. Check expiration
  4. Log click asynchronously via Celery
  5. Redirect to long_url
- **Errors**: 
  - 404 if link not found
  - 410 if link expired
  - 429 if rate limited

### System

#### GET `/health`
- **Purpose**: Health check endpoint
- **Response**: `{ status: "ok" }`

---

## Key Flows

### 1. URL Shortening Flow

```
User → POST /links (with JWT)
  ↓
AuthService.validate_session() → validates JWT against DB
  ↓
LinkService.create_link()
  ↓
  ├─ If custom_code: Check uniqueness, invalidate cache
  └─ If auto-generated: Generate code with retries (max 5)
  ↓
Database: Insert into links table
  ↓
Return Link object to user
```

### 2. Redirect Flow with Analytics

```
User → GET /{code}
  ↓
Rate Limit Check (Redis: ratelimit:redirect:{code})
  ↓
  ├─ If limited → 429 Too Many Requests
  └─ If allowed → Continue
  ↓
Fetch Link (Cache first, then DB)
  ↓
  ├─ Cache hit → Return link from Redis
  └─ Cache miss → Query PostgreSQL, populate cache
  ↓
Check expiration
  ↓
  ├─ If expired → 410 Gone
  └─ If valid → Continue
  ↓
Log Click (Async via Celery)
  ↓
  ├─ Enqueue task to analytics queue
  └─ Fallback to sync if Celery unavailable
  ↓
Celery Worker Processes:
  ├─ Generate idempotency key (prevents duplicates)
  ├─ Check Redis for duplicate
  ├─ Insert into click_events table
  └─ Return success/failure
  ↓
Redirect to long_url
```

### 3. Authentication Flow

```
User → POST /register
  ↓
AuthService.create_user()
  ↓
Hash password with bcrypt
  ↓
Insert into users table
  ↓
Return User object

User → POST /login
  ↓
AuthService.authenticate_user()
  ↓
  ├─ Fetch user by email
  ├─ Verify password with bcrypt
  └─ Return user or null
  ↓
AuthService.create_access_token()
  ↓
  ├─ Generate JWT with user_id
  ├─ Set expiration (30 min default)
  └─ Store token in session_tokens table
  ↓
Return JWT token

Protected Endpoints:
  ↓
get_current_user() middleware
  ↓
AuthService.validate_session()
  ↓
  ├─ Fetch token from session_tokens table
  ├─ Check expiration
  └─ Validate JWT signature
  ↓
Allow access or return 401
```

---

## Key Features

### 1. Caching Strategy
- **Redis caching** for link lookups (cache key: `link:{code}`)
- Cache TTL: 1 hour (3600 seconds)
- Cache invalidation on custom code creation
- Graceful degradation: falls back to DB if Redis unavailable

### 2. Rate Limiting
- Fixed-window rate limiter using Redis
- Limit: 10 requests per 60 seconds per short code
- Key: `ratelimit:redirect:{code}`
- Graceful degradation: allows requests if Redis down

### 3. Async Analytics
- Celery workers process click events asynchronously
- Prevents blocking redirect response
- Idempotency key prevents duplicate counting (5-minute window)
- Fallback to synchronous logging if Celery unavailable
- Automatic retry on transient failures (max 3 retries)

### 4. Full-Text Search
- PostgreSQL full-text search with GIN index
- Searches: code, long_url, tags
- ILIKE fallback if FTS unavailable
- Performance optimized with precomputed search_vector

### 5. Graceful Degradation
- Database unavailable: Returns 503 with clear error
- Redis unavailable: Falls back to DB, allows rate limits
- Celery unavailable: Falls back to sync click logging
- All failures logged with request_id for debugging

### 6. Security
- Stateful JWT authentication (tokens stored in DB)
- bcrypt password hashing
- IP hashing for privacy (click analytics)
- Request ID tracking for error debugging
- SQL injection prevention via ORM

---

## What Was Done in Each Upsk Skill

### 1. System Design Fundamentals (10 modules - Completed)
**Focus**: Building the URL Shortener application

**Key Deliverables**:
- Designed and implemented URL shortener service
- Created database schema with proper indexes
- Implemented authentication with JWT
- Added Redis caching layer
- Integrated Celery for async analytics
- Implemented rate limiting
- Added full-text search capability
- Created graceful degradation patterns

**Modules Covered**:
- System design fundamentals
- Database design and modeling
- API design with FastAPI
- Caching strategies
- Background job processing
- Performance optimization

### 2. Technical Communication (6 modules - Completed)
**Focus**: Documentation and stakeholder communication

**Key Deliverables**:
- Code reviews and feedback
- Technical documentation
- Design documents
- Postmortem templates
- Stakeholder communication strategies

**Modules Covered**:
- Code review best practices
- Technical writing
- Design documentation
- Postmortem analysis
- Stakeholder communication
- Documentation maintenance

### 3. Decomposition & Execution Planning (8 modules - Completed)
**Focus**: Project planning and execution

**Key Deliverables**:
- Requirements extraction from specs
- Dependency mapping with DAGs
- Risk-based task ordering
- Vertical slicing for iterative delivery
- Prescriptive ticket writing
- Interface contracts for parallel work
- Mid-build adaptation strategies
- Integration and verification plans

**Modules Covered**:
- Reading and extracting requirements
- Dependency mapping
- Risk-based ordering
- Vertical slicing
- Ticket writing
- Parallel execution
- Mid-build adaptation
- Integration & verification

**Artifacts Created**:
- Module 1: Full requirements extraction (module-01-full-extraction.md)
- Module 2: Dependency DAG for SkillSwap (module-02-dag.md)
- Module 3: Risk-based build plan (risk-plan-module-03.md)
- Module 4: 5 vertical slices with anti-scope (vertical-slices-module-04.md)
- Module 5: 6 prescriptive tickets (tickets-module-05.md)
- Module 6: 7 interface contracts (contracts-module-06.md)
- Module 7: Blast radius analysis and updated plan (module-07-blast-radius.md, module-07-updated-plan.md)
- Module 8: Integration test plan and scenarios (module-08-integration-test-plan.md, module-08-scenarios.md)

### 4. Debugging & Incident Response (7 modules - Completed)
**Focus**: Systematic debugging, incident handling, and postmortem culture

**Key Deliverables**:
- Debugging pagination, timezone, and log injection bugs in the URL shortener
- Race condition and timestamp corruption analysis
- Performance profiling and ReDoS vulnerability fixes
- Data loss incident simulation and recovery planning
- Cascading failure analysis and system boundary documentation
- Blameless postmortem writing and anti-pattern analysis
- Reflections on real-world incidents (Amazon S3 outage, GitLab, Northeast Blackout, Therac-25)

**Modules Covered**:
- Debugging methodologies and systematic isolation
- Timezone and encoding bugs
- Race conditions and concurrency issues
- Performance bottlenecks and profiling
- Data loss and recovery planning
- Cascading failures and system design
- Blameless postmortem culture

**Artifacts Created**:
- Per-module: break analysis, fix documentation, verification reports, and reflection files
- Notable: `module7_auth_bypass_postmortem.md` with full blameless postmortem rewrite

### 5. Production Readiness (8 modules - Completed)
**Focus**: Hardening services for real-world production environments

**Key Deliverables**:
- Production readiness assessments across 8 modules
- Failure mode analysis for the URL shortener service
- Reflection documents covering observability, SLOs, deployment safety, and on-call practice

**Modules Covered**:
- Observability and structured logging
- SLOs and error budgets
- Safe deployment practices
- On-call and runbook design
- Capacity planning
- Dependency risk and resilience patterns
- Security hardening
- Production launch verification

**Artifacts Created**:
- Per-module: reflection documents and structured report JSON files
- Notable: `module5_failure_modes.md` documenting failure modes and mitigations

### 6. AI-Augmented Engineering (8 modules - Completed)
**Focus**: Using AI tools effectively and responsibly in an engineering workflow

**Key Deliverables**:
- Architecture summaries and trust audits of AI-generated output
- Task tree decomposition with AI assistance
- Code convention verification and context provision
- AI-assisted code review findings
- Iterative prompt refinement logs
- Interface contract generation
- System review and production readiness with AI tooling

**Modules Covered**:
- AI tool orientation and trust calibration
- Task decomposition with AI
- Context provision and prompt engineering
- AI-assisted code review
- Iterative AI collaboration
- Interface and contract generation
- System review with AI
- Production ship verification

**Artifacts Created**:
- `upsk-ai-workspace/progress/ai-augmented-engineering/` — full set of module artifacts
- Notable: `module-01/trust-audit.md`, `module-02/task-tree.md`, `module-03/system-context.md`

---

## Configuration

### Environment Variables (.env)
```env
PORT=8000
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuration Validation
- Port: Must be positive integer
- DATABASE_URL: Required, non-empty
- Redis URL: Defaults to localhost:6379/0
- Secret Key: Defaults to fallback for dev only

---

## Deployment Considerations

### Database Migrations
- Use Alembic for schema versioning
- Migration files in `api/alembic/versions/`
- Run migrations on deployment: `alembic upgrade head`

### Background Workers
- Celery workers required for analytics processing
- Start worker: `celery -A app.celery_app worker --loglevel=info`
- Separate queue: `analytics` for click events
- Worker configuration: 1 task at a time, 1000 tasks per child

### Redis Requirements
- Used for caching, rate limiting, Celery broker
- Connection timeout: 2 seconds
- Graceful degradation if unavailable

### Health Checks
- `/health` endpoint for load balancer probes
- Database connection tested on each request
- Redis connection tested on initialization

---

## Error Handling

### Global Exception Middleware
- Catches all unhandled exceptions
- Generates unique request_id for debugging
- Logs full traceback
- Returns structured error response:
  ```json
  {
    "error": {
      "code": "INTERNAL_SERVER_ERROR",
      "message": "An unexpected error occurred. Please contact support.",
      "request_id": "uuid"
    }
  }
  ```

### Database Unavailability
- Returns 503 with "Database unavailable" message
- Graceful handling in all endpoints

### Redis Unavailability
- Falls back to database operations
- Allows rate limits to pass
- Logs warnings

---

## Performance Optimizations

1. **Database Indexes**:
   - Index on links.created_by for user queries
   - Composite index on click_events(link_id, clicked_at) for analytics
   - GIN index on links.search_vector for full-text search
   - Unique constraint on links.code

2. **Caching**:
   - Link lookups cached in Redis (1 hour TTL)
   - Cache invalidation on updates

3. **Async Processing**:
   - Click logging offloaded to Celery
   - Non-blocking redirects

4. **Connection Management**:
   - Connection timeout: 5 seconds
   - Connection pooling via SQLAlchemy
   - Session cleanup on request completion

---

## Security Considerations

1. **Authentication**:
   - Stateful JWT tokens (stored in DB)
   - Token expiration (30 minutes default)
   - Logout invalidates token immediately

2. **Password Security**:
   - bcrypt hashing with salt
   - Never store plain text passwords

3. **Privacy**:
   - IP addresses hashed (not stored raw)
   - User agent hashed for idempotency

4. **SQL Injection Prevention**:
   - SQLAlchemy ORM prevents injection
   - Parameterized queries for raw SQL

5. **Rate Limiting**:
   - Prevents abuse of redirect endpoints
   - Per-code limits prevent targeting specific links

---

## Monitoring and Observability

### Logging
- Structured logging with request IDs
- Error traces logged to console
- Redis failures logged as warnings
- Celery task IDs logged for tracking

### Analytics
- Click events tracked in database
- User agent, referrer captured
- Time-series data via clicked_at timestamps
- Retention policy: 90 days (configurable)

---

## Future Enhancements (Not Implemented)

Based on Decomposition & Execution Planning Module 7 adaptation:

### SkillSwap Booking System (Planned but not built)
- Role-based access control (employee, manager, department head)
- Company accounts with delegation
- Department-level visibility
- Provider self-service
- Real-time availability
- Payment processing (cut from scope due to timeline)
- Email notifications

These were planned as part of the Decomposition & Execution Planning skill but not implemented due to the CLI state issue blocking progress.

---

## Summary

**Total Skills Completed**: 6
- System Design Fundamentals (10 modules)
- Technical Communication (6 modules)
- Decomposition & Execution Planning (8 modules)
- Debugging & Incident Response (7 modules)
- Production Readiness (8 modules)
- AI-Augmented Engineering (8 modules)

**Total Modules Completed**: 47

**Primary Application**: URL Shortener Service
- Production-ready API with authentication, caching, async processing
- Comprehensive error handling and graceful degradation
- Well-documented with clear architecture and flows

**Planning Artifacts**: Extensive planning documentation for hypothetical SkillSwap booking system demonstrating decomposition, risk assessment, vertical slicing, and integration planning skills.

**Status**: All 6 skills fully completed.
