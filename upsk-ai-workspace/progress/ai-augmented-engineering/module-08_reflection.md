# Module 8 Reflection: Ship It

## Comprehension Questions

1. What core problem does this module solve in ship it?
Bridging gap between "demo-ready" and "production-ready". Demo-ready works on your machine, production-ready works in any environment. Requires regression tests (not just feature tests), documentation for new engineers, CI that catches breakage automatically, deployment strategy with rollback plan. This module is difference between "I built it with AI" and "I shipped it with AI".

2. Which decision in this module has the biggest impact, and why?
Ship readiness strategy (Production-Grade vs Ship and Iterate) has biggest impact. Chose Production-Grade - full test suite, complete documentation, CI pipeline, rollback plan before shipping. Tradeoff: takes longer but won't get shut down day three. Trust costly to rebuild. Five critical tests reveal what's most fragile: privilege escalation, IDOR, concurrent access, reconnection, audit integrity. Ship and Iterate like restaurant without fire suppression inspection - can serve food but risky.

3. What evidence proves the implementation works end-to-end?
Ship verification evidence: auth map lists all endpoints with middleware, input validation documented, test suite passes (8/8 unit, 1/1 integration), secrets audit clean, documentation accurate (three spot-checks), CI green with clean exit code, rollback plan documented. Integration test passes end-to-end: create team, invite member, accept invitation, comment with @mention, activity feed, audit log. All checklist items signed off with evidence.

## Mini Practical Task

STEP 4 verification: CI pipeline evidence
```
Install dependencies... OK
Run migrations... OK
Run unit tests... OK (8/8 passed)
Run integration tests... OK (1/1 passed)
Exit code: 0
Pipeline: GREEN
```

CI runs on clean machine, no local state dependencies.

## Risk and Mitigation

Risk: AI-generated tests depend on generation context - assume pre-existing dev database state. CI failure: test passes locally, fails in CI due to missing records. AI has no concept of environments - writes code that works in environment it can see.

Mitigation: Human review of AI-generated tests for environment assumptions. Require tests create all data in setup phase, clean up in teardown, no hardcoded IDs. Key lesson: check AI-generated tests for environment assumptions - saves hours of CI debugging.

## Key Takeaways

1. Demo-ready vs production-ready: regression tests, documentation for others, CI automation, rollback plan
2. Production-grade strategy: full checklist before shipping prevents day-three shutdowns
3. Five critical tests reveal system fragility - not just happy paths
4. AI-generated tests environment-dependent: written for generation context, not all contexts
5. Human review essential for environmental assumptions in AI tests
