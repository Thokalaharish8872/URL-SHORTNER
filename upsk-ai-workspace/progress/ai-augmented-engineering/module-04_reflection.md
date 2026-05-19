# Module 4 Reflection: Critical Review

## Comprehension Questions

1. What core problem does this module solve in critical review?
AI-generated code has predictable failure modes: security vulnerabilities (IDOR, SQL injection), missing edge cases, poor error handling, confusing naming, inadequate test coverage. Pattern-based review catches systematic issues efficiently. Hybrid approach (pattern-based + targeted line-by-line on high-risk sections like auth, data mutation, permissions) gives 90% thoroughness in 50% time.

2. Which decision in this module has the biggest impact, and why?
Review method decision (line-by-line vs pattern-based vs hybrid). Chose pattern-based with targeted line-by-line on high-risk sections. This is most impactful because AI failure modes are predictable - pattern-based catches majority of systematic bugs in 10-15 minutes vs 40-60 minutes for full line-by-line. Targeted line-by-line on auth/permissions catches critical issues pattern-based might miss.

3. What evidence proves the implementation works end-to-end?
Code review findings documented: 2 CRITICAL (IDOR on DELETE/PUT teams), 2 HIGH (no name validation, no unique constraint), 1 MEDIUM (generic errors). IDOR vulnerability on invitation endpoint fixed with specific authorization check. Edge case tests confirmed bugs exist before fix. Admin/non-admin verification tests confirm fix works. Fix prompt specific enough to produce correct implementation.

## Mini Practical Task

STEP 4 verification: Edge case testing for IDOR fix.
- Admin user POST /teams/{id}/invitations: Expected 201, Actual 201 ✓
- Non-admin user POST /teams/{id}/invitations: Expected 403, Actual 403 ✓

Proof: Tests confirm authorization check works correctly.

## Risk and Mitigation

Risk: One review pass is necessary but not sufficient. Complex features need 2-3 passes. Fixes may introduce new issues (AI's auth check fix might have bug under concurrent access). 

Mitigation: Multiple review passes for complex features. Targeted line-by-line on high-risk sections. Automated testing for regression detection. Code review by multiple engineers.

## Key Takeaways

1. Five predictable AI failure modes: security, edge cases, error handling, naming, tests
2. Pattern-based review efficient for AI code - catches systematic issues in 10-15 minutes
3. Hybrid approach: pattern-based + targeted line-by-line on high-risk (auth, data mutation, permissions)
4. IDOR common AI bug - AI adds auth (common pattern) but misses domain-specific ownership checks
5. Security is contextual - depends on your domain, roles, business rules. AI doesn't have this context unless provided
