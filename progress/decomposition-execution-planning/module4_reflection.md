# Module 4 Reflection: Vertical Slicing

## Comprehension Questions

1. **What core problem does this module solve in vertical slicing?**
   This module teaches breaking work into thin, end-to-end slices that go from database to API to UI for specific user actions. It teaches distinguishing horizontal layers (data, backend, UI) from vertical slices (feature threads), writing explicit anti-scope to prevent scope creep, and using acceptance criteria that non-technical people can verify.

2. **Which decision in this module has the biggest impact, and why?**
   The decision on what goes in the first slice (supply side vs demand side) has the biggest impact because it determines what hypothesis you test first. Choosing demand side (browse and book with hardcoded providers) tests the core value proposition immediately, whereas supply side (provider registration) leaves the core question unanswered. The first slice sets the direction for all subsequent slices.

3. **What evidence proves the implementation works end-to-end?**
   Defined 5 vertical slices (plus payment spike) with explicit scope, anti-scope, dependencies, acceptance criteria, and complexity estimates. Slice 1 is ultra-thin (2-3 hours) with specific anti-scope (10+ items excluded). Added Slice 1.5 payment spike to address investor pressure while preserving thin first slice. Each slice has human-testable acceptance criteria (no "check database" steps).

## Mini Practical Task

**STEP 4 verification for vertical slicing:**

**Verification action:** Clickthrough test for Slice 1 - verified it can be tested without reading code. User experience walkthrough from opening browser to seeing confirmation page requires no technical knowledge. Learned whether booking flow UX makes sense to users (product insight, not technical confirmation). Anti-scope is specific with 10+ excluded items, protecting against "where is search?" questions.

**Proof:** In module4_verification.md, documented clickthrough test with 7 UI steps and identified ONE product learning (booking flow UX). Confirmed no red flags - not too thick (2-3 hours), not too thin (has behavior), anti-scope specific, acceptance criteria human-testable.
