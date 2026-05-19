# Module 3 Race Condition Bug: Concurrent Analytics Writes

## Symptom
Intermittent 500 errors on popular short links. Not every request, not on every link. Error appears a few times per hour unpredictably.

## Reproduction Strategy
Chose **Synthetic Reproduction (Option B)** - write a script to simulate suspected conditions (concurrency) rather than replaying production traffic.

## Phase 1: Form Hypothesis
Popular links receive more concurrent redirects. The error is intermittent and depends on timing - suggests a race condition.

## Phase 2: Minimal Reproduction Script

**Python script**:
```python
import asyncio
import aiohttp

SHORT_CODE = "test-link"
CONCURRENCY = 10
BASE_URL = f"http://localhost:8000/{SHORT_CODE}"

async def make_request(session):
    async with session.get(BASE_URL, allow_redirects=False) as resp:
        return resp.status

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session) for _ in range(CONCURRENCY)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if isinstance(r, int) and r in (301, 302)]
    errors = [r for r in results if isinstance(r, int) and r == 500]
    exceptions = [r for r in results if isinstance(r, Exception)]

    print(f"Results: {len(successes)} redirects, {len(errors)} errors, {len(exceptions)} exceptions")

    if errors:
        print("BUG REPRODUCED: 500 errors under concurrent load")
    else:
        print("No errors this run. Try again or increase CONCURRENCY.")

asyncio.run(main())
```

**Key characteristic**: Changes exactly one variable - sends 10 simultaneous requests instead of one at a time. Minimal moving parts.

## Phase 3: Run and Observe
Running the script produces 500 errors in most runs. Server logs show:
```
ERROR: duplicate key value violates unique constraint "analytics_link_id_bucket_unique"
DETAIL: Key (link_id, timestamp_bucket)=(42, 2024-01-15T14:00) already exists.
```

## Phase 4: Trace Root Cause

**Redirect handler flow**:
1. Look up short link by code
2. Check if analytics row exists for (link_id, current_timestamp_bucket)
3. If no row exists, INSERT with count = 1
4. If row exists, UPDATE to increment count
5. Send 301 redirect

**Race condition** (check-then-act pattern):
```
Request A: SELECT ... WHERE link_id=42 AND bucket='14:00' -> no row found
Request B: SELECT ... WHERE link_id=42 AND bucket='14:00' -> no row found
Request A: INSERT (42, '14:00', count=1) -> success
Request B: INSERT (42, '14:00', count=1) -> CRASH: unique constraint violation
```

Both requests checked. Both saw nothing. Both inserted. The second one lost the race.

## Phase 5: Implement Fix

**Fix**: Use PostgreSQL upsert (INSERT ... ON CONFLICT DO UPDATE) - an atomic operation.

```sql
INSERT INTO analytics (link_id, timestamp_bucket, count)
VALUES ($1, $2, 1)
ON CONFLICT (link_id, timestamp_bucket)
DO UPDATE SET count = analytics.count + 1;
```

**Why this works**:
- Eliminates check-then-act pattern entirely
- No separate SELECT needed
- Database handles "does it exist?" check and insert/update in single atomic step
- Two concurrent upserts cannot conflict - database serializes internally

## Phase 6: Verify Fix

Run reproduction script 10 times. Should see zero 500 errors across all runs. Verify analytics data: after 10 concurrent requests, row should show count of exactly 10 (not 1 from lost writes, not 20 from double counting).

## Key Insight

**Reproduction script value**: The 20-line script is worth more than the fix itself. The fix was easy (single SQL query change). The hard part was seeing the bug. The script:
- Turns "it sometimes breaks" into "it breaks every time I run this"
- Becomes a permanent test suite artifact
- Runs in CI to prevent reintroduction
- The fix solves today's problem, the script prevents tomorrow's

## Lessons

1. **Minimal reproduction**: Change exactly one variable at a time
2. **Race conditions depend on timing**: Code looks correct for single request, fails under concurrent load
3. **Check-then-act is dangerous**: Always use atomic operations for concurrent access
4. **Upsert eliminates race conditions**: Database handles existence check and update atomically
5. **Reproduction scripts are test artifacts**: They prevent regression and enable team verification
