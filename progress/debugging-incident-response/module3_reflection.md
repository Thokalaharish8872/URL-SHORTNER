# Module 3 Reflection: Reproduction Science

## Comprehension Questions

### 1. What core problem does this module solve in reproduction science?
The module solves the problem of turning "it sometimes breaks" into "it breaks every time I run this script." It teaches variable isolation - changing exactly one variable at a time (concurrency) to reproduce intermittent bugs. The core skill is creating minimal reproduction cases that isolate the trigger variable, distinguishing flaky from deterministic failures, and understanding that almost all "flaky" bugs are actually deterministic with a trigger you haven't found yet.

### 2. Which decision in this module has the biggest impact, and why?
Choosing synthetic reproduction over production replay has the biggest impact. Synthetic reproduction is fast to write (minutes vs hours/days for replay setup), safe (no real user data privacy risk), portable (any team member can run it), and forces thinking about causation which sharpens understanding. The 20-line reproduction script is worth more than the fix itself - the fix was easy (single SQL query), the hard part was seeing the bug. The script becomes a permanent test artifact that prevents regression.

### 3. What evidence proves the implementation works end-to-end?
For the race condition fix: Run reproduction script 10 times with 10 concurrent requests each. Should see zero 500 errors across all runs. Analytics count should be exactly 10 (not 1 from lost writes, not 20 from double counting). For the timestamp fix: Run reproduction script 5 times, verify `last_accessed_at` matches the timestamp of the last request in server logs exactly (within database precision). Both count and timestamp should be correct every time.

## Mini Practical Task

### STEP 4 Verification: Reproduction Science

**Task**: Verify race condition fix with minimal reproduction script

**Reproduction script**:
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

    print(f"Results: {len(successes)} redirects, {len(errors)} errors")

    if errors:
        print("BUG REPRODUCED")
    else:
        print("NO ERRORS")

asyncio.run(main())
```

**Verification**:
```bash
# Run 10 times
for i in {1..10}; do
  python repro_race.py
done

# Check analytics
SELECT link_id, count, last_accessed_at FROM analytics WHERE link_id = 42;
```

**Expected proof**:
- All 10 runs show "NO ERRORS" (zero 500 responses)
- Analytics count = 10 (correct, no lost writes)
- `last_accessed_at` matches timestamp of last request in logs

## Risk and Mitigation

### Risk
**Lost update race condition**: Separate UPDATE queries for count and timestamp can execute out of order, causing silent data corruption where later timestamps are overwritten by earlier ones.

### Mitigation
**Atomic upsert with GREATEST()**: Combine count and timestamp updates into single atomic operation using PostgreSQL upsert with `GREATEST(analytics.last_accessed_at, EXCLUDED.last_accessed_at)` to keep the later timestamp regardless of execution order. This eliminates the lost update pattern entirely.

## Key Takeaways

1. **Minimal reproduction changes one variable**: Isolate the trigger (concurrency) without adding complexity
2. **Reproduction scripts are test artifacts**: They prevent regression and enable team verification
3. **Check-then-act is dangerous**: Always use atomic operations for concurrent access
4. **Lost updates are silent**: No errors, just wrong data - must verify all fields not just the obvious ones
5. **Almost all flaky bugs are deterministic**: They have triggers you haven't found yet
