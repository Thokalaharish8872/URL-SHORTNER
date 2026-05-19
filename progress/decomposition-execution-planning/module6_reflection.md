# Module 6 Reflection: Parallel Execution

## Comprehension Questions

1. **What core problem does this module solve in parallel execution?**
   This module teaches managing parallel workstreams so that independently produced outputs actually integrate. It teaches writing interface contracts (shared data shapes, types, error formats), choosing parallelism strategies (isolated branches vs shared context), designing synchronization points (end-only vs checkpoints), and detecting and fixing contract violations when agents deviate from specifications.

2. **Which decision in this module has the biggest impact, and why?**
   The parallelism strategy decision (isolated branches vs shared context) has the biggest impact. Isolated branches prevent merge conflicts during development but push integration to merge time where contract violations are caught late. Shared context enables continuous integration but risks agents stepping on each other with merge conflicts. The wrong choice determines whether integration is continuous or a painful separate step.

3. **What evidence proves the implementation works end-to-end?**
   Created 7 interface contracts covering database schema, ticket-to-ticket dependencies, and future integration points. Verified contracts by walking through Sarah booking scenario end-to-end from GET /api/providers through POST /api/bookings. Identified and fixed contract violation (Unix timestamps vs ISO 8601 dates) by diffing agent output against contract. Re-verified scenario after fix confirmed no mismatches remain.

## Mini Practical Task

**STEP 4 verification for parallel execution:**

**Verification action:** Contract verification - pointed to ID type specification (UUID v4 in Contract 1), error format specification ({error: message} in Contracts 2-4), datetime format specification (ISO 8601 in Contract 1). Identified field not consumed: user_id in POST /api/bookings is nullable for Slice 1 anonymous bookings. Walked through Sarah booking scenario tracing through agents' code, confirmed response shapes match contracts, race condition handled by validating slot status='available' before booking.

**Proof:** In module6_verification.md, documented contract verification with specific line references, end-to-end scenario trace with actual JSON request/response examples, and race condition handling (409 error if slot booked between view and confirm).
