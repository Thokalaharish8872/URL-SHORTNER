# Module 7 Reflection: Security & Architecture Review

## Comprehension Questions

1. What core problem does this module solve in security & architecture review?
AI cannot judge business logic correctness, security in context, architectural coherence, data integrity under pressure, compliance requirements. Individual code review catches function bugs, system-level review catches interaction bugs. AI-assisted scan + manual critical path review balances speed and thoroughness - AI finds patterns humans miss, humans catch semantic issues AI misses.

2. Which decision in this module has the biggest impact, and why?
Security review scope decision (AI-assisted hybrid vs full manual) has biggest impact. AI first-pass scan finds patterns across all code efficiently, human manual review on critical path (auth, permissions, data mutation, roles, personal data) catches semantic issues. Full manual too slow - loses focus after 18 files. AI scanner has blind spots (trained on same patterns as generator) but human critical path review compensates. Time allocation on auth/permissions is most effective.

3. What evidence proves the implementation works end-to-end?
Security findings document: 1 CRITICAL (role management no permission tests), 2 HIGH fixed. Privilege escalation fixed with 6 explicit constraints, 13 test cases all pass. Auth map created, input validation audit, IDOR check completed. Cross-team access test: User A cannot access Team 2 resources. Full test suite green after fixes. No regressions. Architecture: pattern consistency OK, naming consistency OK, error handling OK.

## Mini Practical Task

STEP 4 verification: Privilege escalation fix verification.
- Viewer tries to update own role to admin: 403 ✓
- Admin updates viewer to member: 200 ✓
- Owner promotes member to owner: 200 ✓
- Invalid role "superadmin": 400 ✓

13 test cases all pass.

## Risk and Mitigation

Risk: AI scanner has same blind spots as generator - won't catch "normal" AI-generated mistakes. Human critical path review may miss if not rigorous. Individual findings compose into exploits when combined (membership check without permission level + no role validation = privilege escalation).

Mitigation: Human manual review on critical path (auth, permissions, data mutation). Specific fix prompts with multiple explicit constraints (6 constraints for privilege escalation fix). System-level review catches combination of findings that create exploits. Cross-team access testing catches IDOR.

## Key Takeaways

1. Five categories AI cannot judge: business logic, security in context, architectural coherence, data integrity under pressure, compliance
2. AI checks syntax, humans check semantics - AI validates structure, humans validate intent
3. AI-assisted scan + manual critical path balances speed and thoroughness
4. Individual findings compose into exploits - system-level review essential
5. Specific security fix prompts with multiple constraints - not vague "fix security"
