# Module 6 Interlude: Mars Climate Orbiter Reflection

## Question 1: What kind of testing would have caught the units mismatch?

**Contract testing** - automated verification that both sides of an interface agree on the format and semantics of shared data. Unit tests verify individual components work correctly in isolation. Integration tests verify components work together within a team's boundary. But contract testing specifically verifies the interface boundary between two independent workstreams.

A contract test would have:
- Taken the actual output from the SIS (newton-seconds)
- Fed it to the navigation software expecting pound-force-seconds
- Failed immediately when the values were off by factor 4.45
- Failed even though both pieces of software had zero bugs internally

The failure mode is insidious because the system doesn't crash - it produces wrong answers quietly. Contract testing catches this by explicitly validating that the assumptions embedded in data (units, ranges, formats) match across the boundary.

## Question 2: What are the "units" in my parallel execution?

**Date formats:** Contract specifies ISO 8601 strings ("2025-03-15T14:30:00Z"). One agent could use Unix timestamps (1710512400) for "efficiency." Both are valid dates, but they don't match. The frontend displays raw integers instead of formatted dates.

**ID types:** Contract specifies UUID v4 ("550e8400-e29b-41d4-a716-446655440000"). One agent could use auto-incrementing integers (7). Both uniquely identify records, but they don't match. API calls between services fail with validation errors.

**Status enums:** Contract specifies lowercase ("confirmed", "failed"). One agent could use uppercase ("CONFIRMED", "FAILED") by convention. Status comparisons like `status === "confirmed"` never match. Confirmation emails never send.

**Null-handling:** Contract specifies user_id is nullable for anonymous bookings. One agent could assume user_id is always required. Booking creation fails for Slice 1 anonymous users.

**How to know before it's too late:**
- Write contract tests that validate response shapes against contract schemas
- Run these tests in CI before merge
- Use shared type definitions that both agents import
- Pre-merge checklist that includes "verify response shapes match contract"
- Code generation from contract (OpenAPI spec generates both server stubs and client types)
