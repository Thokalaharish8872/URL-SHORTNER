# Module 6 Reflection: Graceful Degradation

## Comprehension Questions

### 1. What core problem does this module solve in graceful degradation?
The module solves the problem of slow dependencies being more dangerous than down dependencies. When a dependency is slow, requests hang waiting for timeouts, connection pools fill up, and the entire service cascades into failure. The module teaches circuit breakers to stop calling failing dependencies, retry with exponential backoff and jitter to avoid thundering herds, and aggressive timeouts to free resources immediately. The core problem is preventing a single slow dependency from taking down the entire service.

### 2. Which decision in this module has the biggest impact, and why?
The timeout strategy decision (aggressive vs conservative) has the biggest impact. Aggressive timeouts (500ms-1s) keep the server healthy by freeing connections, threads, and memory immediately during degradation. Conservative timeouts (5-10s) cause connection pool exhaustion - 100 req/s holding connections for 10s = 1000 simultaneous connections, freezing the entire service. The difference between a 30-second recovery and a 5-minute recovery. Aggressive timeouts reject 2% of valid requests but prevent full service hang, which is the right trade-off for production reliability.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: All external calls have explicit timeouts (500ms-1s). Circuit breaker opens after threshold (5 failures) when database stopped. Fallback response fast (under 100ms) with circuit open, fallback does not depend on external service. Backoff visible in logs - retry logs show increasing delays (100ms, 200ms, 400ms) with jitter (not exact values). Circuit closes after recovery - database restart causes circuit to transition through half-open to closed, normal responses resume. Fixed runaway retry failure by capping max retries at 3, preventing resource exhaustion.

## Mini Practical Task

### STEP 4 Verification: Circuit Breaker State Transitions

**Task**: Verify circuit breaker opens and closes correctly during database outage

**Commands**:
```bash
# Stop database
docker stop postgres

# Hit API repeatedly
for i in {1..10}; do curl http://localhost:3000/api/users/1; done

# Check logs - should see:
# - Timeout log lines at 500ms
# - Failures accumulating
# - "circuit_opened" after 5 failures
# - "circuit_open_fallback" for remaining requests (under 100ms)

# Restart database
docker start postgres

# Wait for recovery timeout (30s)
sleep 30

# Hit API again
curl http://localhost:3000/api/users/1

# Check logs - should see:
# - "circuit_half_open" - one trial request
# - Trial request succeeds
# - "circuit_closed" - normal operation resumes
```

**Proof**: Logs show full state machine: closed -> open (after 5 failures) -> half-open (after recovery timeout) -> closed (after successful trial). Fallback responses under 100ms when circuit open. Normal responses resume after database recovery. Circuit breaker prevents cascading failure during database outage.

## Risk and Mitigation

### Risk
**Runaway retries causing resource exhaustion**: If maximum retry count is not capped or set to Infinity, a single slow request generates hundreds of retries, each spawning a new timer and holding resources. CPU usage spikes, memory climbs, process becomes unresponsive. This is a denial-of-service attack against your own service triggered by a slow dependency.

### Mitigation
**Cap maximum retry count**: Set explicit maximum retry limit (e.g., 3 attempts). Ensure retry loop has exit condition that stops after configured count regardless of error type. Log every retry with attempt number and delay. Without cap, slow requests cause cascading failure. With cap, requests fail fast and free resources, allowing the dependency to recover.

## Key Takeaways

1. **Slow is more dangerous than down**: Down triggers immediate error handling, slow drains resources until collapse. Aggressive timeouts prevent this by failing fast.
2. **Circuit breaker state machine**: Closed (normal), Open (tripped, fallback responses), Half-open (testing recovery). Half-open state is critical for automatic recovery.
3. **Retry with exponential backoff and jitter**: Exponential backoff gives dependency breathing room (100ms, 200ms, 400ms). Jitter spreads out retries to prevent thundering herd (synchronized waves hammering recovering service).
4. **Aggressive timeouts over conservative**: 500ms timeout frees connections 10x faster than 5s timeout. Connection pool exhaustion causes full service hang, which is worse than occasional rejected valid requests.
5. **Fallback must be fast and independent**: Fallback response must be under 100ms and not depend on the failing dependency. If fallback queries the database, it's not a fallback - it's wishful thinking.
