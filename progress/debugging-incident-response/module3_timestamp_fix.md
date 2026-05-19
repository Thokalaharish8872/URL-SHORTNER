# Module 3 Fix: Timestamp Lost Update Race Condition

## Root Cause
The redirect handler performs two database operations:
1. Upsert for count (atomic, safe under concurrency)
2. Separate UPDATE for `last_accessed_at` (not atomic, vulnerable to lost update)

**Lost update race condition**:
```
Scenario 1 (correct order):
Request A (T=100ms): upsert count
Request B (T=102ms): upsert count
Request A: UPDATE last_accessed_at = T=100ms
Request B: UPDATE last_accessed_at = T=102ms  <-- correct

Scenario 2 (wrong order):
Request A (T=100ms): upsert count
Request B (T=102ms): upsert count
Request B: UPDATE last_accessed_at = T=102ms
Request A: UPDATE last_accessed_at = T=100ms  <-- WRONG, A overwrites B
```

Under concurrency, execution order is not the same as arrival order. The last UPDATE to execute wins, regardless of which request actually arrived last. Result: `last_accessed_at` shows T=100ms when actual last access was T=102ms.

## Fix

Combine count update and timestamp update into single atomic upsert:

```sql
INSERT INTO analytics (link_id, timestamp_bucket, count, last_accessed_at)
VALUES ($1, $2, 1, NOW())
ON CONFLICT (link_id, timestamp_bucket)
DO UPDATE SET
  count = analytics.count + 1,
  last_accessed_at = GREATEST(analytics.last_accessed_at, EXCLUDED.last_accessed_at);
```

**Key insight**: `GREATEST()` function keeps whichever value is later - the existing one or the new one. Even if updates execute out of order, the timestamp always reflects the most recent access.

**Alternative simpler fix**:
```sql
DO UPDATE SET
  count = analytics.count + 1,
  last_accessed_at = NOW();
```

This accepts that timestamp reflects "when database processed the update" rather than "when request arrived." For most analytics purposes this is fine, but GREATEST is more correct when request-arrival timestamps matter.

**Critical**: Remove the separate UPDATE query. Everything must happen in the single upsert to maintain atomicity.

## Verification

Run reproduction script 5 times with 10 concurrent requests each. Check:
1. Count is 10 (should still be correct)
2. `last_accessed_at` matches timestamp of last request in server logs (exactly, within database precision)

Expected result: Timestamp correct every time, no silent data corruption.

## Key Lessons

1. **Lost updates are silent**: No errors, no crashes, just wrong data
2. **Separate operations break atomicity**: Two queries = two opportunities for race conditions
3. **GREATEST() protects against out-of-order updates**: Keeps the later timestamp regardless of execution order
4. **Combine operations for atomicity**: Single upsert handles both count and timestamp atomically
5. **Check all data fields**: Silent corruption hides in fields you're not watching (count was correct, timestamp was wrong)
