# Module 3 Reflection: Design Documents & RFCs

## Comprehension Questions

1. **What core problem does this module solve in design documents & RFCs?**
   This module solves the problem of design documents that fail to prevent mistakes because they're missing critical sections (alternatives), hide assumptions as facts, or have vague risk mitigations that can't be executed in emergencies.

2. **Which decision in this module has the biggest impact, and why?**
   The lightweight vs heavyweight format decision has the biggest impact because it determines whether the document gets written and reviewed at all. A lightweight RFC that's actually read and reviewed is better than a heavyweight doc that sits unread. However, the format must still include the essential sections (alternatives, open questions, specific mitigations).

3. **What evidence proves the implementation works end-to-end?**
   The fixed design document (event_pipeline_fixed.md) demonstrates the implementation works: it includes genuine alternatives section, moves hidden assumptions to open questions with validation plans, and has concrete risk mitigations with specific thresholds and procedures.

## Mini Practical Task

**STEP 4 verification for rate_limiting_rfc.md:**

**Alternatives section excerpt:**
"Alternative 1: Fixed-window rate limiting in application code
- Pros: Simple to implement, no Redis dependency
- Cons: Doesn't work across multiple servers, bursty traffic at minute boundaries, no centralized admin"

**Change made:** Added genuine alternatives with real pros/cons instead of strawman alternatives. Each alternative has genuine advantages over the proposed approach.
