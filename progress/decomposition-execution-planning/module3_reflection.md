# Module 3 Reflection: Risk-Based Ordering

## Comprehension Questions

1. **What core problem does this module solve in risk-first ordering?**
   This module teaches identifying risk types (integration, novelty, dependency, scale, business/legal), scoring uncertainty, and ordering work to retire the biggest unknowns early. It teaches distinguishing risk from dependency, using spikes to test assumptions, and planning around business blockers with stubbed interfaces.

2. **Which decision in this module has the biggest impact, and why?**
   The decision to tackle the scariest thing first has the biggest impact. If you delay high-risk items and discover they don't work late in the project, you waste weeks of work built on false assumptions. Front-loading risk means early failures are cheap (2 hours for a spike) rather than expensive (90 days of UI work on a broken API assumption).

3. **What evidence proves the implementation works end-to-end?**
   The revised risk plan with 14 items: front-loaded high-risk items (availability management with concurrency, payment interface stub), distinguished business/legal risks from technical risks, created stubbed interface to continue work around business blocker, escalated to PM with timeline request. The plan shows team can continue progress on 13 items while payment integration is blocked.

## Mini Practical Task

**STEP 4 verification for risk-first ordering:**

**Verification action:** Distinguished risk (uncertainty) from dependency (blocking). Auth is low-risk but high-dependency - built early to unblock risky items, not because auth itself is risky. Payment processing is high-risk (integration, business blocker) but lower-dependency. This distinction prevents confusing critical-path items with risky items.

**Proof:** In module3_verification.md, explicitly stated "Auth is low-risk, high-dependency. I put auth early not because it's risky, but because it unblocks risky items." This shows understanding that foundational items are not the same as risky items.
