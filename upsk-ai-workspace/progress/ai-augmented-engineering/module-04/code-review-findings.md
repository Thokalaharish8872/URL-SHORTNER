# Code Review Findings - Module 4

## File: api/app/models.py (Team model addition)

| Category | Finding | Severity | Evidence |
|----------|---------|----------|----------|
| Security | No validation that owner_id references existing user | High | Line: owner_id field has no database-level validation |
| Edge Cases | No constraint on team name uniqueness | Medium | Two teams could have same name |
| Error Handling | N/A | N/A | Data model |
| Naming | Follows existing convention (PascalCase Team) | Low | Good |
| Tests | N/A | N/A | Model file |

## File: api/app/models.py (TeamMembership model addition)

| Category | Finding | Severity | Evidence |
|----------|---------|----------|----------|
| Security | No check that user_id and team_id combination is unique | High | Could have duplicate memberships |
| Edge Cases | No constraint preventing self-invitation via direct insert | Medium | User could add themselves to team |
| Error Handling | N/A | N/A | Data model |
| Naming | Follows existing convention (PascalCase TeamMembership) | Low | Good |
| Tests | N/A | N/A | Model file |

## File: api/app/main.py (Team CRUD endpoints)

| Category | Finding | Severity | Evidence |
|----------|---------|----------|----------|
| Security | No admin check on DELETE /teams/{id} - any authenticated user can delete | Critical | Line: DELETE endpoint only checks authentication, not ownership |
| Security | No admin check on PUT /teams/{id} - any authenticated user can update | Critical | Line: PUT endpoint only checks authentication, not ownership |
| Edge Cases | No validation that team name is not empty string | High | Could create team with empty name |
| Error Handling | Generic error handling - returns 500 for database errors | Medium | Should return specific error messages |
| Naming | Follows existing convention (snake_case functions) | Low | Good |
| Tests | N/A | N/A | No test file generated |

## FIX LIST -- Priority Order
==========================

1. [CRITICAL] IDOR on DELETE /teams/{id} - no ownership check
   File: api/app/main.py
   Fix: Add middleware to verify req.user is team owner before delete

2. [CRITICAL] IDOR on PUT /teams/{id} - no ownership check
   File: api/app/main.py
   Fix: Add middleware to verify req.user is team owner before update

3. [HIGH] No validation on team name emptiness
   File: api/app/schemas.py
   Fix: Add Pydantic validator to ensure name is not empty string

4. [HIGH] No unique constraint on team name
   File: api/app/models.py
   Fix: Add unique=True to name field

5. [HIGH] Duplicate membership possible
   File: api/app/models.py
   Fix: Add UniqueConstraint on (team_id, user_id)
