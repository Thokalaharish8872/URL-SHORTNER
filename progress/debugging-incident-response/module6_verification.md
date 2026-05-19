# Module 6 Verification: Cascading Failure and Cache Invalidation

## Bug #10 Causal Chain (From Memory)

1. Queue job fails (bad data, temporary DB hiccup, any error)
2. Queue worker retries immediately (no backoff delay configured)
3. Each retry acquires a database connection from the shared pool
4. The retry fails again (same error that caused original failure)
5. Worker retries again immediately (no maximum retry count configured)
6. Steps 3-5 repeat in a tight loop
7. Shared connection pool is exhausted within seconds (all connections checked out)
8. API requests that need the database cannot get a connection (all pool slots occupied)
9. API requests hang indefinitely, waiting for connections that never free up
10. Entire API becomes unresponsive (requests queue up, timeouts)
11. Health checks (which also need database connections) time out
12. Monitoring reports the API as down

**Steps in chain**: 12 steps from initial job failure to API down
**Longest gap between cause and symptom**: Step 1 (queue job failure) to Step 12 (API down) - crosses 4 system layers (queue → worker → database pool → API → monitoring)
**Time gap**: Can be seconds to minutes depending on pool size and retry rate

## Bug #9: Why Nobody Noticed During Development

**Real answer**: The bug is invisible during normal development workflow because:
1. **Delete operation rarely tested manually**: Developers mostly create and read links during testing, rarely delete them
2. **Cache TTL masks the bug**: With 5-minute TTL, the stale data "fixes itself" before a developer would notice - if they delete a link and test it immediately, it still works (redirects) because cache still has the data
3. **Manual QA timing**: If a tester deletes a link and checks it 30 seconds later, it still works. If they check 6 minutes later, they might notice but by then they've moved on to other tests
4. **No automated tests for delete-then-access pattern**: Test suites likely test "create link" and "read link" but not the sequence "delete link, wait < TTL, try to access"
5. **Cache invalidation not tested**: The code path for cache invalidation on delete is rarely exercised in development

**The development workflow made this invisible**: The combination of rarely testing deletes, long cache TTL, and lack of automated integration tests for the delete-then-access pattern meant the bug could exist for months without detection.

## Monitoring Alert to Catch Bug #10 Early

**Single metric**: Connection pool utilization percentage

**Threshold**: Alert when pool utilization exceeds 80% for more than 30 seconds

**Why this catches it early**: Step 7 in the causal chain is "connection pool exhausted" - this is the earliest detectable signal in the chain. Before the API goes down (step 12), before health checks timeout (step 11), the connection pool utilization spikes. A queue worker in a tight retry loop would cause pool utilization to jump from normal (~20-30%) to 100% within seconds. Alerting at 80% gives you time to intervene before the pool is fully exhausted and the API becomes unresponsive.

**Alternative earliest signal**: Queue retry rate - alert when retry rate exceeds X per minute. But connection pool utilization is more direct and easier to correlate with the actual symptom (API unresponsiveness).

## Red Flags Addressed

### Can trace causal chain?
**Yes**: Can reproduce the 12-step chain from memory, including the specific design flaws (no backoff, no max retry, shared pool) and the mechanism by which queue worker behavior exhausts the pool that API needs.

### Fix for Bug #9 is not "lower cache TTL"
**Correct**: The proper fix is explicit cache invalidation on delete, not lowering TTL. Lowering TTL from 5 minutes to 30 seconds still leaves a 30-second window where deleted links redirect - that's still stale data serving to users. Explicit invalidation (cache.delete(link_code) on delete operation) ensures immediate consistency.

### Fix for Bug #10 is not "increase connection pool"
**Correct**: Increasing pool size treats the symptom, not the cause. A bigger pool just means the exhaustion takes slightly longer (30 seconds instead of 5). The correct fix addresses the root cause: exponential backoff to prevent tight retry loops, maximum retry count to stop infinite retries, and separate connection pools for resource isolation (bulkheads principle).
