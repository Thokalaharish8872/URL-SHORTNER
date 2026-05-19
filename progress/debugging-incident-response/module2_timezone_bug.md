# Module 2 Bug #4: Timestamp Timezone Mismatch

## Symptom
User report: "Links I create around midnight sometimes return 404 for a few hours, then magically start working. It does not happen every time. It only seems to happen late at night."

This is:
- Intermittent
- Time-dependent
- Self-fixing (links "reappear" after a few hours)

## Step 1: Read Logs as Timeline

**Investigation**: Find a case where a link was created near midnight. Compare timestamps in logs vs database.

**Expected finding**:
- Log timestamp: `2025-01-15T23:58:00.000Z` (UTC)
- Database timestamp: `2025-01-15T18:58:00.000-05:00` (Eastern time) or `2025-01-15T18:58:00` (no timezone indicator)

These look like different times because they ARE different times if timezone is not accounted for.

## Step 2: Understand the Mismatch

**Root Cause**: Two systems speaking different time dialects.

- **Application logs**: Use UTC (Coordinated Universal Time - global standard)
- **Database**: Stores timestamps in server's local timezone (or no timezone indicator)

**The problem**: When a link is created at 11:58 PM UTC (6:58 PM server-local time):
- Database records: 6:58 PM (local time)
- Application queries for "today" using UTC midnight as boundary
- Database interprets "today" using local midnight (5 hours away)
- Link falls into the gap - invisible to application's queries
- Link "reappears" when local clock crosses midnight too

**Analogy**: Scheduling a meeting at "6" - you mean 6 PM Eastern, friend assumes 6 PM Pacific. You show up at same place at different times, each thinks the other is late.

## Step 3: Trace in Code

**Expected findings**:
- Application logger uses UTC (standard and correct)
- Database stores timestamps in server's local timezone (or without timezone indicator)
- Lookup query compares these incompatible values

**Code locations to check**:
- Timestamp creation in application (models.py, services.py)
- Database configuration (db.py, PostgreSQL config)
- Query that looks up links (services.py list_links, get_link_by_code)

## Step 4: Fix

**Universal rule**: Store everything in UTC, convert to local time only at display layer.

**Fix steps**:
1. Configure database to store timestamps in UTC
2. Ensure application writes UTC timestamps to database
3. Ensure all queries use UTC comparisons
4. Add timezone indicator to all timestamp columns if missing
5. Convert to local time only when displaying to users

**Specific fixes for URL shortener**:
- Database connection string: Ensure `timezone=utc` parameter
- SQLAlchemy models: Ensure `DateTime(timezone=True)` on all timestamp columns
- Application code: Use `datetime.now(timezone.utc)` instead of `datetime.now()`
- Queries: Use UTC-aware datetime comparisons

## Step 5: Verify

**Verification steps**:
1. Create a link
2. Check log timestamp (should be UTC)
3. Check database timestamp (should match log, both in UTC)
4. Create a link near midnight UTC
5. Confirm it resolves immediately, not after timezone delay
6. Query for links created "today" using UTC midnight

**Expected result**: All timestamps match in UTC, queries work correctly at all times, no 404s around midnight.

## Key Lessons

1. **Never store local time in database** - Always use UTC for storage
2. **Never compare UTC to local time** - Ensure all comparisons use same timezone
3. **Convert at display layer only** - Human-readable times are UI concern, not storage concern
4. **Timezone bugs are intermittent and self-fixing** - They appear at specific times and "fix themselves" when clocks align, making them easy to dismiss
5. **Add timezone indicators** - Storing timestamps without timezone info (naive datetime) creates ambiguity
