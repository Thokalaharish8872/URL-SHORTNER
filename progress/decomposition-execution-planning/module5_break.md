# Module 5 Break: AI Agent Output Analysis

## Problems with AI Agent's Booking Endpoint

Looking at my Ticket 4 (POST /api/bookings), similar problems could occur:

### Problem 1: No Authentication
**What was missing:** My ticket said "No authentication required for this ticket (auth is separate)" but didn't specify whether user_id should come from session or request body. The agent could make the endpoint public where anyone passes any user_id.

**Cross-cutting concern:** Authentication policy is a project-wide standard. Should be in a shared document referenced by all tickets, not repeated in each ticket. But my ticket should explicitly state "user_id must come from authenticated session" or reference the auth standard document.

**Scope impact:** Small addition - just a note about auth requirements.

### Problem 2: No Rate Limiting
**What was missing:** My ticket didn't mention rate limiting at all. An agent could create an endpoint with no protection against abuse.

**Cross-cutting concern:** Rate limiting policy is a project-wide standard. Should be in a shared document. But my ticket should either include rate limiting requirements or reference the standard.

**Scope impact:** Small addition - "Apply standard rate limiting policy (see docs/rate-limiting.md)" or specify "100 requests per minute per IP."

### Problem 3: Generic Error Handling for Unexpected Errors
**What was missing:** My ticket specified error responses for 400, 404, 409 but not for unexpected errors (database timeout, connection pool exhausted). Agent lets these bubble up as 500 with stack traces.

**Cross-cutting concern:** Error handling conventions are project-wide standards. Should be in a shared document. But my ticket should reference the standard or specify "Use global error handler (see docs/error-handling.md)."

**Scope impact:** Small addition - reference to error handling standard.

### Problem 4: No Logging
**What was missing:** My ticket didn't ask for logging. Agent added no audit trail.

**Cross-cutting concern:** Logging standards are project-wide. Should specify what gets logged (request ID, user action, timestamp) in a shared document. My ticket should reference the logging standard.

**Scope impact:** Small addition - "Log booking creation with request ID and user ID per docs/logging.md."

## Diagnosis

All four problems are cross-cutting concerns that belong in project-wide standards documents (auth policy, rate limiting policy, error handling conventions, logging standards). However, my tickets failed to reference these standards. Silence is not a reference.

I need to either:
1. Add a "Standards References" section to each ticket that links to the relevant project-wide docs
2. Or create these standards documents and reference them
3. Or for this exercise, add brief notes to tickets about cross-cutting concerns like auth, rate limiting, error handling, and logging

For prescriptive tickets aimed at AI agents, it's safer to include brief explicit requirements for these cross-cutting concerns rather than relying on referenced standards that may not exist.
