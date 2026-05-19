# Module 5 Fix: Unstated Assumptions and Ticket Revisions

## Three More Unstated Assumptions in Ticket 4

1. **Input validation for data types:** The ticket specifies fields are UUIDs but doesn't say what happens if a client sends a string instead of a UUID. Should the endpoint validate UUID format before querying the database?

2. **Character encoding for text fields:** The interface contract mentions strings but doesn't specify character encoding (UTF-8). What happens if a client sends non-UTF-8 data?

3. **Null handling:** The request body fields are not explicitly marked as nullable or non-nullable. What happens if provider_id is null or empty string?

## Applied to Remaining Tickets

I've updated Ticket 4 with:
- Rate limiting (100 req/min per IP)
- Logging requirements
- Global error handler reference
- SQL injection prevention
- Idempotency for booking creation

Applied similar fixes to Tickets 2 and 3 (provider endpoints):
- Added rate limiting
- Added logging requirements
- Added global error handler reference
- Added input validation (UUID format)

Applied to Tickets 5 and 6 (auth endpoints):
- Added rate limiting (stricter: 10 req/min per IP for auth)
- Added logging for auth events
- Added global error handler reference
- Added password strength validation (already in scope)

## Completeness Checklist

- ✅ Every endpoint specifies every status code it can return (200, 400, 404, 409, 401, 500)
- ✅ Every request body specifies required vs optional fields
- ✅ Every response body shows exact JSON shape with field names and types
- ⚠️ Authentication/authorization requirements stated (some tickets say "none for now" which is explicit)
- ✅ Every ticket specifies behavior on unexpected errors (global error handler)
- ⚠️ Ticket outputs match next ticket inputs (need to verify booking_id format is consistent across tickets)
