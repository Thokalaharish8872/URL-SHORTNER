# Module 7 Break: Bad Postmortem Analysis

## Problems Found in the Postmortem

### Summary
**Problem**: Too vague - "The database went down on Friday afternoon"
**Should be**: Specific incident description with severity, duration, affected systems

### Timeline
**Problem**: Imprecise times - "Friday afternoon", "Friday evening", "Saturday morning"
**Should be**: Precise UTC timestamps (14:23 UTC, 18:45 UTC, etc.)

### Root Cause
**Problem**: Blames a person - "John deployed the broken migration without testing it first"
**Should be**: "The deployment pipeline did not enforce migration testing as a prerequisite for production deployment"
**Issue**: Subject is a person (John), not a system. Cannot remediate by changing John.

### Contributing Factors
**Problem**: All blame people, not systems
- "John did not test the migration locally" → Should be: "The migration tool does not have a dry-run mode"
- "The team was in a rush" → Should be: "The deployment process lacks a mandatory cooldown period"
- "Nobody reviewed John's PR because everyone was busy" → Should be: "The code review process does not require approval for database migrations"

**Issue**: Every factor has a human subject. None can be fixed by changing systems.

### Impact
**Problem**: Vague - "Some users could not log in for a while"
**Should be**: "45,000 users unable to log in for 3 hours (18:00-21:00 UTC)"
**Issue**: No specific numbers, no duration, no business impact assessment

### Resolution
**Problem**: Too brief - "We rolled back the migration"
**Should be**: "Database was restored from backup at 21:15 UTC, migration was rolled back using point-in-time recovery, service resumed at 21:30 UTC"
**Issue**: No details on how resolution was achieved

### Remediation Items
**Problem**: All are terrible
1. "Developers should test migrations before deploying" - Asks humans to be better, not systemic fix
2. "John will have all future PRs reviewed" - Targets specific person, not process change
3. "Try to avoid deploying on Fridays" - Vague, no owner, no deadline, not actionable

**Should be**:
1. "Add automated migration testing to CI pipeline that requires dry-run validation before production deployment" (Owner: Platform team, Deadline: End of sprint)
2. "Require mandatory code review approval for all database migrations" (Owner: Engineering manager, Deadline: End of sprint)
3. "Implement deployment freeze on Fridays after 14:00 UTC" (Owner: Release engineering, Deadline: End of sprint)

**Issue**: Remediations ask people to change behavior instead of changing systems. "Try to avoid" is not actionable.

### Lessons Learned
**Problem**: Blame people, not systemic
- "John needs to be more careful" - Blame, not systemic
- "We should not deploy on Fridays" - Vague, not actionable

**Should be**:
- "The deployment process lacked guardrails for high-risk operations like database migrations"
- "No automated validation prevented the broken migration from reaching production"

## Summary of Failures

This postmortem is an **incident report pretending to be a postmortem**. It answers "what happened" but fails to answer "what do we change so this class of failure cannot happen again."

**Every section fails the blameless test**:
- Root cause blames John
- Contributing factors blame John, the team, busy people
- Remediations ask John and developers to be better
- Lessons learned tell John to be more careful

**No systemic changes proposed**:
- No process changes
- No tool changes
- No architecture changes
- Only requests for humans to "be more careful"

**This postmortem will not prevent recurrence** because it treats the symptom (John made a mistake) rather than the disease (the system allowed John's mistake to reach production without validation).
