# Task Tree: Team Collaboration Feature

## Task 1: Create Team Data Model and Migration
**Task name**: Create Team data model and database migration

**Input context needed**:
- Reference existing User model at `api/app/models.py`
- Reference existing migration pattern in `api/alembic/versions/`
- Reference database configuration at `api/app/db.py`

**Expected output**:
- New Team model added to `api/app/models.py` with fields: id (UUID, primary key), name (string, required, max 100 chars), description (string, optional, max 500 chars), owner_id (UUID, foreign key to users.id, required), created_at (timestamp), updated_at (timestamp)
- New Alembic migration file in `api/alembic/versions/` creating teams table with foreign key constraint to users

**Acceptance criteria**:
- Run migration: `alembic upgrade head` succeeds
- Query database: `SELECT * FROM teams` returns empty table with correct schema including owner_id foreign key
- Import model: `from app.models import Team` succeeds without errors

**Dependencies**: None (foundational task)

**Interface Contract (produced for Task 2)**:
- Table: teams with columns id (UUID), name (string), owner_id (FK to users.id), description (string), created_at (timestamp), updated_at (timestamp)
- Every team has exactly one owner identified by owner_id
- owner_id is required (NOT NULL)

---

## Task 2: Create Team Membership Model and Migration
**Task name**: Create TeamMembership model and database migration

**Input context needed**:
- Reference User and Team models at `api/app/models.py`
- Reference existing migration pattern in `api/alembic/versions/`

**Expected output**:
- New TeamMembership model added to `api/app/models.py` with fields: id (UUID, primary key), team_id (foreign key to teams.id), user_id (foreign key to users.id), role (enum: admin, member, viewer), joined_at (timestamp)
- New Alembic migration file creating team_memberships table with foreign key constraints

**Acceptance criteria**:
- Run migration: `alembic upgrade head` succeeds
- Query database: team_memberships table exists with correct foreign keys
- Import model: `from app.models import TeamMembership` succeeds

**Dependencies**: Task 1 (Team model must exist first)

**Interface Contract (expects from Task 1)**:
- Table: teams exists with columns id (UUID), name (string), owner_id (FK to users.id)
- team_id foreign key references teams.id
- owner_id foreign key references users.id
- Team owner is separate from TeamMembership role (owner is in teams table, membership is in team_memberships table)

**Shared contract**: Both tasks agree that team ownership is handled by owner_id in teams table, while membership and roles are handled by TeamMembership table

---

## Task 3: Create Team CRUD API Endpoints
**Task name**: Create team CRUD API endpoints

**Input context needed**:
- Reference Team model at `api/app/models.py`
- Reference existing API pattern at `api/app/main.py`
- Reference Pydantic schemas at `api/app/schemas.py`

**Expected output**:
- New Pydantic schemas in `api/app/schemas.py` for TeamCreate, TeamResponse
- New API endpoints in `api/app/main.py`: POST /teams (create), GET /teams/{id} (read), GET /teams (list), PUT /teams/{id} (update), DELETE /teams/{id} (delete)
- TeamService class in `api/app/services.py` for business logic

**Acceptance criteria**:
- POST /teams with valid data returns 201 with team object
- POST /teams with missing name returns 400 validation error
- GET /teams/{id} for existing team returns 200 with team object
- GET /teams/{id} for non-existent team returns 404
- DELETE /teams/{id} returns 204 and removes team from database

**Dependencies**: Task 1 (Team model must exist first)

---

## Task 4: Create Invitation Data Model and Migration
**Task name**: Create Invitation data model and database migration

**Input context needed**:
- Reference User and Team models at `api/app/models.py`
- Reference existing migration pattern in `api/alembic/versions/`

**Expected output**:
- New Invitation model in `api/app/models.py` with fields: id (UUID, primary key), team_id (foreign key to teams.id), inviter_id (foreign key to users.id), invitee_email (string, required), status (enum: pending, accepted, expired, revoked), token (string, unique), expires_at (timestamp), created_at (timestamp)
- New Alembic migration file creating invitations table

**Acceptance criteria**:
- Run migration: `alembic upgrade head` succeeds
- Query database: invitations table exists with correct schema
- Import model: `from app.models import Invitation` succeeds

**Dependencies**: Task 1 (Team model must exist first)

---

## Task 5: Create Invitation API Endpoint
**Task name**: Create invitation API endpoint

**Input context needed**:
- Reference Invitation model at `api/app/models.py`
- Reference API pattern at `api/app/main.py`
- Reference Pydantic schemas at `api/app/schemas.py`

**Expected output**:
- Pydantic schemas for InvitationCreate, InvitationResponse in `api/app/schemas.py`
- POST /teams/{team_id}/invitations endpoint in `api/app/main.py`
- InvitationService in `api/app/services.py` with create_invitation method
- Token generation using secrets module

**Acceptance criteria**:
- POST /teams/{team_id}/invitations with valid email returns 201 with invitation object
- POST with invalid email returns 400 validation error
- Invitation token is unique and generated
- Invitation has expires_at set to 7 days in future

**Dependencies**: Task 4 (Invitation model must exist first), Task 3 (Team API must exist for validation)

---

## Task 6: Implement Email Sending for Invitations
**Task name**: Implement email sending for invitations

**Input context needed**:
- Reference Invitation model at `api/app/models.py`
- Reference Redis client at `api/app/redis_client.py`
- Check if email service exists in project (Twilio SendGrid or similar)

**Expected output**:
- Email service integration (SendGrid or similar) in `api/app/services.py`
- Background task in `api/app/tasks.py` to send invitation emails
- Email template with invitation link containing token
- Queue email sending via Celery

**Acceptance criteria**:
- Creating invitation queues email task
- Email is sent to invitee_email with valid invitation link
- Email task logs success/failure
- Email sending failure does not block invitation creation

**Dependencies**: Task 5 (Invitation endpoint must exist first)

---

## Task 7: Create Invitation Acceptance Endpoint
**Task name**: Create invitation acceptance endpoint

**Input context needed**:
- Reference Invitation model at `api/app/models.py`
- Reference TeamMembership model at `api/app/models.py`
- Reference API pattern at `api/app/main.py`

**Expected output**:
- GET /invitations/{token}/accept endpoint in `api/app/main.py`
- Logic to validate token, check expiry, create TeamMembership, update Invitation status
- Handle edge cases: already member, invalid token, expired token

**Acceptance criteria**:
- GET /invitations/{token}/accept with valid token returns 200 and creates team membership
- Invalid token returns 404
- Expired token returns 400 with error message
- User already in team returns 400 with error message

**Dependencies**: Task 4 (Invitation model), Task 2 (TeamMembership model), Task 5 (Invitation endpoint)

---

## Task 8: Create Role-Based Access Control Middleware
**Task name**: Create role-based access control middleware

**Input context needed**:
- Reference TeamMembership model at `api/app/models.py`
- Reference API pattern at `api/app/main.py`
- Reference existing middleware patterns if any

**Expected output**:
- RBAC middleware function in `api/app/main.py` or separate file
- Decorator or dependency injection for FastAPI routes
- Logic to check user role on team before allowing action
- Error handling for unauthorized access (403)

**Acceptance criteria**:
- Non-member accessing team resource returns 403
- Member accessing admin-only resource returns 403
- Admin accessing admin resource succeeds (200)
- Middleware can be applied to specific routes

**Dependencies**: Task 2 (TeamMembership model), Task 3 (Team API endpoints)

---

## Critical Path
**Longest dependency chain**: Task 1 → Task 2 → Task 3 → Task 8 (Team model → TeamMembership → Team API → RBAC)
**Alternative chain**: Task 1 → Task 4 → Task 5 → Task 6 → Task 7 (Team model → Invitation → Invitation API → Email → Acceptance)

**Critical path determines minimum time to ship**: 4 sequential tasks on first chain, 5 on second. Can parallelize after Task 1.

## Riskiest Task
**Task 6: Email sending for invitations**
- Risk: External service integration (SendGrid/Twilio) may fail or have API changes
- Risk: Email deliverability issues (spam filters, invalid emails)
- Risk: Background task queue (Celery) configuration may be complex
- Reasoning: Integration with external systems is most likely to surface unexpected issues. Email sending adds infrastructure complexity beyond database and API logic.

## Task Granularity
**Choice**: Medium-grained (8 tasks)
**Reasoning**: Each task produces 50-150 lines of code. Sweet spot for review thoroughness while keeping prompt count manageable. Each task is substantial enough to feel like progress but small enough to review thoroughly. Aligns with 150-line constraint.
