# Module 3 Break: Silent Data Corruption - Timestamp Race Condition

## Symptom
After fixing the race condition with upsert, a new issue emerged. The analytics row has:
- Correct redirect count (10 requests = count of 10)
- Incorrect `last_accessed_at` timestamp - doesn't match the actual timestamp of the last request

This is **silent data corruption**:
- No errors in logs
- No 500 responses
- No alerts
- Just quietly incorrect data that will mislead queries

## Investigation

Run reproduction script with 10 concurrent requests. Check analytics row:
- Redirect count: Correct (10)
- `last_accessed_at`: Wrong (off by milliseconds, or corresponds to an earlier request in the batch, not the last)

Compare database timestamp to actual timestamp from logs (Module 02 logs have precise timestamps now).

## Root Cause

The upsert fixed the count race condition but introduced a new race condition for the timestamp.

**Current upsert logic**:
```sql
INSERT INTO analytics (link_id, timestamp_bucket, count, last_accessed_at)
VALUES ($1, $2, 1, $3)
ON CONFLICT (link_id, timestamp_bucket)
DO UPDATE SET count = analytics.count + 1, last_accessed_at = $3;
```

**The problem**: When multiple concurrent requests execute the upsert simultaneously:
- Request A upserts with timestamp T1, sets last_accessed_at = T1
- Request B upserts with timestamp T2, sets last_accessed_at = T2
- Request C upserts with timestamp T3, sets last_accessed_at = T3

All three succeed (no unique constraint violation because upsert handles it), but the final `last_accessed_at` value depends on which request's UPDATE clause executes last. This is non-deterministic - it might be T1, T2, or T3, not necessarily the latest timestamp (T3 if T3 > T2 > T1, but timing is unpredictable).

**Why this happens**: The upsert is atomic for the INSERT/UPDATE decision, but the UPDATE clause is not atomic across concurrent executions. Multiple concurrent upserts can all execute their UPDATE clauses, and the final value is whichever UPDATE happened to execute last.

## Fix

**Option 1: Use database-generated timestamp**
```sql
INSERT INTO analytics (link_id, timestamp_bucket, count, last_accessed_at)
VALUES ($1, $2, 1, NOW())
ON CONFLICT (link_id, timestamp_bucket)
DO UPDATE SET count = analytics.count + 1, last_accessed_at = NOW();
```

Use `NOW()` in the UPDATE clause instead of the application-provided timestamp. The database evaluates `NOW()` at execution time, so the last UPDATE will set the most recent database time.

**Option 2: Use a separate atomic update for timestamp**
After the upsert, issue a separate UPDATE that only sets the timestamp:
```sql
UPDATE analytics
SET last_accessed_at = $3
WHERE link_id = $1 AND timestamp_bucket = $2;
```

This is less ideal because it's a second operation (not atomic with the count increment).

**Option 3: Use a sequence or trigger**
Create a database trigger that updates `last_accessed_at` on every UPDATE, using the transaction timestamp.

**Recommended fix**: Option 1 - use `NOW()` in the upsert UPDATE clause. This ensures the timestamp is always set to the database's current time at the moment of the last successful UPDATE, which will be the most recent.

## Verification

Run reproduction script again. Check:
- Redirect count: Should be 10
- `last_accessed_at`: Should match the timestamp of the last request in the logs (within a few milliseconds of the final request)

The timestamp should be the latest among all concurrent requests, not an earlier one.
