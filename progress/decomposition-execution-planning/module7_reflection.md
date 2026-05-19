# Module 7 Reflection: Mid-Build Adaptation

## Comprehension Questions

1. **What core problem does this module solve in mid-build adaptation?**
   This module teaches adapting plans when requirements change mid-execution. It teaches blast radius assessment to identify what artifacts are affected, preserving completed work rather than starting over, categorizing tickets as MUST/SHOULD/CUT to manage timeline compression, layering changes on existing plans rather than rewriting from scratch, and communicating impact honestly to stakeholders when scope grows.

2. **Which decision in this module has the biggest impact, and why?**
   The decision between Option B (Minimal Bridge) and Option A (Proper Modeling) has the biggest impact. Option B allows shipping the demo in 6 days but creates technical debt. Option A is architecturally correct but would miss the deadline. The role-based access requirement pushed Option B to its limit ("maximal bridge") - the hack grew into multiple tables, role-based middleware, and JWT changes. Choosing Option B was the right call because missing the demo costs funding, but acknowledging the increased complexity was critical for credibility.

3. **What evidence proves the implementation works end-to-end?**
   Updated blast radius analysis three times (company accounts, timeline compression, role-based access) layering changes on existing structure. Updated plan preserved original categorization while escalating impacts (4 tickets from NO IMPACT/MINOR to MAJOR, payment processing cut from SHOULD SHIP to CUT). Updated impact statement explicitly acknowledged contradiction with original plan and explained why payment processing was cut. Demonstrated ability to absorb two requirement changes in 15 minutes without losing coherence or starting over.

## Mini Practical Task

**STEP 4 verification for mid-build adaptation:**

**Verification action:** Blast radius assessment for role-based access requirement. Identified artifacts that escalated from NO IMPACT to MAJOR (POST /api/auth/login, Ticket 1 Seed Database) and MINOR to MAJOR (POST /api/auth/register, Registration form). Added new artifacts (roles table, departments table, JWT contract). Decision re-evaluation: Option B becoming expensive with role complexity but staying with it due to 6-day deadline constraint. Updated impact statement to acknowledge payment processing cut and explain scope tradeoff to PM.

**Proof:** In module7_fix.md, documented structural layering (built on adaptation not revert to scratch), role-based access approach (roles in data model, JWT carries role, middleware enforces permissions), and plan version count (3 changes in module). In module-07-blast-radius.md, added "Change 3: Role-Based Access Control" section with escalation analysis and decision re-evaluation.
