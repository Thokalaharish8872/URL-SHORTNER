# Module 1 Interlude: Therac-25 Reflection

## The Therac-25 Incident
Between 1985-1987, the Therac-25 radiation therapy machine massively overdosed at least 6 patients, killing 3. The manufacturers (AECL) refused to believe the machine could fail because:
- Diagnostics showed normal operation
- Logs showed green
- Error-checking routines found nothing
- They believed the software worked correctly

Fritz Hager, a hospital physicist, reproduced the race condition by methodically testing different key sequences and timings. He started from the hypothesis "the machine can fail" and designed tests to prove it.

## Reflection Questions

### 1. Ensuring Hypotheses Are Genuinely Testable
**Problem**: AECL engineers had a hypothesis they couldn't disprove - "the software works correctly." They ran diagnostics that could only confirm their belief.

**Solution**: A good hypothesis must be falsifiable. To ensure testability:
- **Define what would disprove it**: If the hypothesis is "database is down," the disconfirming test is a successful connection. If connection succeeds, hypothesis is wrong.
- **Design disconfirming tests first**: Ask "under what conditions could this be false?" before asking "how can I prove this is true?"
- **Avoid confirmation bias**: Don't only run tests that could confirm your belief. Run tests that could eliminate it.
- **Test the negative case**: If you think "X causes Y," also test "what happens when X is absent?"

**Example from Module 1**:
- Hypothesis 1: "Database is down" → Test: Try to connect. If successful, hypothesis is disproven.
- Hypothesis 2: "Environment variable missing" → Test: Check env vars. If missing, hypothesis is confirmed.

### 2. Safety Nets That Might Be Silently Catching Bugs
**Insight**: The race condition existed in Therac-20 for years, but hardware interlocks masked it. The bug was firing but invisible because another layer caught the failure.

**Safety nets in my systems that might be masking bugs**:
- **Redis caching**: If cache returns stale data, database bugs might be hidden
- **Celery retries**: Transient failures are retried automatically, hiding flaky code
- **Graceful degradation**: If Redis is down, code falls back to DB - might hide Redis connection issues
- **Rate limiting**: Prevents abuse but might hide performance issues
- **Error middleware**: Catches exceptions and returns generic errors, might hide specific failures
- **Database connection pooling**: Hides connection leaks until pool exhaustion

**What would break if removed**:
- Without Redis caching: Database load increases, might reveal slow queries
- Without Celery retries: Flaky tasks fail immediately, expose race conditions
- Without graceful degradation: Redis failures become visible immediately
- Without rate limiting: Performance bottlenecks exposed under load

**Action**: Periodically test with safety nets disabled to ensure underlying code is robust.

### 3. Trusting Telemetry Over Human Reports
**Problem**: Patients reported burning, shock, pain. Operators checked logs (green) and concluded patients were mistaken.

**When I've trusted telemetry over humans**:
- Assuming "500 error" means database issue without checking configuration
- Trusting "operation successful" logs when users report problems
- Dismissing user reports as "user error" when metrics look fine
- Believing health check endpoints that return 200 but don't test critical paths

**What it would take to trust humans over telemetry**:
- **Take reports seriously**: Even if logs look fine, investigate user reports
- **Reproduce manually**: Don't rely only on automated tests - try to reproduce the user's exact steps
- **Check multiple data sources**: Logs, metrics, user reports, and manual testing
- **Acknowledge telemetry limitations**: Logs can be incomplete, metrics can have gaps, health checks can be shallow
- **Design for observability**: Ensure critical user journeys are instrumented, not just technical metrics

**Lesson**: When a human says "something is wrong" and the dashboard says "everything is fine," the human is often right. The dashboard might be measuring the wrong thing, or the bug might be in a layer the dashboard doesn't see.

## Key Takeaways

1. **Falsifiability is essential**: A hypothesis you cannot disprove is not a hypothesis - it's a belief
2. **Safety nets mask bugs**: Caches, retries, and fallbacks can hide problems that exist but are caught
3. **Trust user reports**: When telemetry contradicts human experience, investigate the human report
4. **Design disconfirming tests**: Always ask "what would prove this wrong?" before asking "what would prove this right?"
5. **Test without safety nets**: Periodically disable fallbacks to ensure core code is robust
