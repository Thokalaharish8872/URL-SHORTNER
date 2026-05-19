# Module 3 Micro-Exercise: Race Conditions and Flaky Bugs

## Concepts

**Race Condition**: Two operations check state, find it acceptable, and act on it without knowing the other operation is doing the same thing simultaneously. Example: Two requests read database, both see no existing row, both try to insert - second insert crashes. Depends on timing - code looks fine for single request, explodes when two correct things happen at wrong time.

**Flaky vs Deterministic**:
- **Deterministic**: Happens every time you perform the same action (broken light switch - always fails)
- **Flaky**: Sometimes works, sometimes doesn't (flickering light - works 9/10 times)

**Critical insight**: Almost every "flaky" bug is actually deterministic - it just has a trigger you haven't found yet. "It's flaky" means "I don't know which variable controls it."

## Micro-Exercise Answers

### Question 1: Three questions to narrow down "app is slow sometimes"

**Question 1**: When is it slow? What time of day, day of week, or traffic level?
- This identifies if it's load-related (peak hours) or time-dependent (cron jobs, backups)

**Question 2**: Which specific actions or pages are slow? Is it all operations or specific endpoints?
- This narrows down whether it's a systemic issue or specific to certain code paths

**Question 3**: What changed around the time it became slow? New deployment, configuration change, database migration, or infrastructure change?
- This identifies if it's a recent regression or long-standing issue that was just noticed

**What "sometimes" is hiding**:
- Traffic volume (high vs low load)
- Database connection pool exhaustion
- Cache hit/miss patterns
- Third-party API latency
- Background job execution timing
- Network latency to specific regions

### Question 2: "I cannot reproduce it" vs "it is not reproducible"

**"I cannot reproduce it"**: A statement about me/my debugging skills. I haven't figured out how to trigger it yet. This is honest and accurate.

**"It is not reproducible"**: A claim about the universe - that the bug is inherently non-deterministic. This is almost always false. The bug has a trigger, I just haven't found it.

**Which to say in standup**: "I cannot reproduce it" - because it's honest and doesn't close the door on investigation. Saying "it's not reproducible" creates a false sense that the bug is random, which leads to accepting it as inevitable instead of hunting for the trigger.

## Key Takeaways

1. **Race conditions depend on timing** - code looks correct for single request, fails under concurrent load
2. **Flaky bugs are actually deterministic** - they have triggers you haven't found yet
3. **"I cannot reproduce it" is honest** - "it's not reproducible" is almost always false
4. **Find the variable** - your job is to identify what controls the "sometimes" behavior
5. **Concurrency triggers are common** - many "flaky" bugs are actually race conditions that only appear under specific load patterns
