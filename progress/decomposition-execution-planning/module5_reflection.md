# Module 5 Reflection: Ticket Writing

## Comprehension Questions

1. **What core problem does this module solve in task specification?**
   This module teaches writing precise, prescriptive tickets that another developer or AI agent can execute without asking questions. It teaches the 7-section format (Title, Context, Scope, Interface Contract, Acceptance Criteria, Constraints, Anti-Scope), distinguishing spec gaps from implementation decisions, and identifying unstated assumptions in security, operational, data, and integration categories.

2. **Which decision in this module has the biggest impact, and why?**
   The decision about ticket format (prescriptive vs intent) has the biggest impact. Prescriptive tickets specify everything (function signatures, file locations, exact response shapes) which is critical for AI agents with zero context. Intent tickets leave the "how" to the executor, which works for experienced humans but produces garbage from AI agents. The wrong format choice determines whether tickets are executable or just wishes.

3. **What evidence proves the implementation works end-to-end?**
   Created 6 tickets using the 7-section format with complete interface contracts (request/response bodies, status codes, database schemas), human-testable acceptance criteria using Given/When/Then, explicit constraints including rate limiting, logging, error handling, and input validation. Fixed spec gaps identified by AI agent roleplay (auth, rate limiting, error handling, logging) and applied to all tickets. Completeness checklist shows all tickets now specify status codes, required vs optional fields, exact JSON shapes, auth requirements, error handling behavior.

## Mini Practical Task

**STEP 4 verification for task specification:**

**Verification action:** AI agent roleplay on Ticket 2 identified 3 questions: port (spec gap), file location (implementation decision), database library (spec gap). Fixed spec gaps by adding port 8080, pg library, DATABASE_URL env variable to Constraints. Applied learning to all tickets by adding rate limiting (200/min for regular endpoints, 10/min for auth), logging requirements, global error handler references, input validation (UUID format, password strength, time validation), and security constraints (SQL injection prevention, constant-time password comparison, idempotency).

**Proof:** In module5_verification.md and module5_fix.md, documented the 3 questions, classified them as spec gaps vs implementation decisions, and listed 3 additional unstated assumptions (data type validation, character encoding, null handling). Updated all 6 tickets in tickets-module-05.md with the fixes.
