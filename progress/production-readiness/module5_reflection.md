# Module 5 Reflection: Failure Mode Analysis

## Comprehension Questions

### 1. What core problem does this module solve in failure mode analysis?
The module solves the problem of reacting to failures instead of anticipating them. It teaches how to enumerate ALL ways a system can break before it happens, so you can decide how to handle each failure calmly rather than at 3 AM during an incident. The core problem is that "slow" is more dangerous than "down" - down triggers immediate error handling, slow drains resources until collapse. Failure mode analysis is a fire drill for your service.

### 2. Which decision in this module has the biggest impact, and why?
The failure stance decision (fail-closed vs fail-open) has the biggest impact. Fail-closed rejects requests entirely if dependency is down, never producing incorrect behavior but trading availability for correctness. Fail-open continues with degraded behavior, serving defaults or cached values, allowing users to use the product but risking incorrect behavior. The default stance should be fail-closed for security-critical dependencies (auth, fraud check, payments) with selective fail-open for non-critical features (recommendations). This decision affects every dependency interaction.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Failure mode table has 16 entries covering database (connection refused, slow queries, pool exhaustion), cache (down, stale data), external APIs (SendGrid, Twilio, Firebase - down and slow), infrastructure (disk full, OOM, DNS failure, network partition). Two failures simulated: database stopped (30s hang then 500), 1ms timeout (unhandled exception). Each failure has desired handling different from current handling. DNS resolution failure added to table after BREAK exercise. Transient vs permanent failures classified correctly.

## Mini Practical Task

### STEP 4 Verification: Failure Mode Table

**Task**: Verify failure mode table has comprehensive coverage and handling strategies

**Verification**:
Failure mode table entries:
- Database: connection refused (503, retry with backoff), slow queries (timeout 5s, return 504), pool exhaustion (pool timeout 5s, alert)
- Cache: down (fall through to database), stale data (TTL expiry, cache-aside)
- External APIs: down (circuit breaker, queue for retry), slow (timeout 5s, circuit breaker)
- Infrastructure: disk full (disk usage alert at 80%), OOM (memory limit, heap usage alert), DNS failure (health check, cached IPs), network partition (circuit breakers)

**Proof**: Table covers 16 distinct failure modes with specific probability assessments, user impacts, current handling (mostly unhandled), and desired handling (graceful degradation). Risk surface identified: 12 of 16 entries show crash/hang/unhandled - this is the prioritized list of things to fix. DNS resolution failure was missed initially and added after BREAK exercise.

## Risk and Mitigation

### Risk
**Slow dependencies more dangerous than down**: If a dependency responds 100x slower than normal (8 seconds instead of 50ms), the service waits indefinitely. Connection pools fill up. Threads exhaust. The entire service collapses even though the dependency is technically "up". Down triggers immediate error handling, slow causes resource exhaustion and cascading failure.

### Mitigation
**Strict timeouts and circuit breakers**: Every external call must have a strict timeout (e.g., 5 seconds). If the timeout is exceeded, fail fast rather than waiting. Circuit breakers stop calling a slow dependency after repeated failures, returning cached fallback or error instead. This prevents slow dependencies from draining resources. Distinguish transient failures (retry with backoff) from permanent failures (fail fast, don't retry).

## Key Takeaways

1. **Failure mode analysis is proactive**: Think about failures before they happen, not during a 3 AM incident. Decide how to handle each failure calmly.
2. **Slow is more dangerous than down**: Down triggers immediate error handling, slow drains resources until collapse. Every external call needs a timeout.
3. **Fail-closed default, selective fail-open**: Default to fail-closed for correctness (never produce incorrect behavior). Use fail-open selectively for non-critical features where degraded experience is acceptable.
4. **Distinguish transient vs permanent**: Transient failures (network blips, connection timeouts) should retry with backoff. Permanent failures (invalid credentials, schema errors) should fail fast without retrying.
5. **Risk surface is prioritized list**: The failure mode table is a prioritized list of things that will hurt you, ranked by probability multiplied by impact. Use it to guide what to fix first.
