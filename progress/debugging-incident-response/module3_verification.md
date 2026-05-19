# Module 3 Verification: Race Condition Reproduction

## Question 1: What was the variable that made this bug appear?

**Variable**: Concurrency - the number of simultaneous requests.

**How I know**:
- Tested with single request: No error
- Tested with 10 concurrent requests: Error reproduced
- Data shape didn't matter (same short code, same URL)
- Timing didn't matter (not time-of-day dependent, not load-dependent)

**Why data and timing were not contributing factors**:
- Data: Used same short code in both single and concurrent tests - only concurrency changed
- Timing: Bug triggered immediately on concurrent load, not at specific times or under specific load patterns

**Evidence**: The reproduction script changes exactly one variable (10 concurrent requests vs 1) and reliably produces the error.

## Question 2: Single curl command vs thorough testing

**Would single curl find it?** No. A single curl command sends one request at a time. The race condition only appears when multiple requests hit the same code path simultaneously.

**What this tells about testing gap**:
- "I tested it" often means "I tested the happy path with single requests"
- "I tested it thoroughly" means testing edge cases, concurrency, and failure modes
- Race conditions are invisible to single-request testing
- The gap between "works" and "works under load" is where production bugs hide

**Lesson**: Testing must simulate real-world conditions including concurrent access, not just single sequential requests.

## Question 3: Could this race condition exist elsewhere?

**Pattern to look for**: SELECT followed by INSERT (check-then-act pattern).

**Other endpoints with potential race conditions**:
- Link creation: If checking for duplicate custom_code with SELECT then INSERT
- User registration: If checking for email existence with SELECT then INSERT
- Session token creation: If checking for existing token with SELECT then INSERT
- Any "get or create" pattern where code checks existence then creates if not found

**Specific locations to audit**:
- `LinkService.create_link()` - custom_code uniqueness check
- `AuthService.create_user()` - email uniqueness check
- `AuthService.create_access_token()` - session token creation
- Any analytics aggregation with SELECT-then-UPDATE pattern

**Fix pattern**: Replace all check-then-act patterns with atomic operations (upsert, unique constraints with proper handling, or database-level serialization).

## Question 4: Why 10 concurrent requests?

**Why 10**: Provides high probability of race condition without overwhelming the system. With 10 simultaneous requests, the window between SELECT and INSERT is likely to be hit by at least 2 requests.

**What if 2**: Might not trigger reliably - depends on timing. Two requests might execute sequentially by chance.

**What if 1000**: Would almost certainly trigger but would overwhelm the system, potentially causing other issues and making it hard to isolate the specific race condition.

**Minimum concurrency level**: Likely 3-5 concurrent requests would reliably trigger, but 10 provides comfortable margin while remaining manageable for local testing.

**What this tells about production likelihood**:
- If bug triggers with 10 concurrent requests, it will definitely trigger in production under real load
- Popular links receive hundreds/thousands of concurrent redirects
- The fact that error appeared "a few times per hour" in production suggests concurrency level is naturally occurring
- Production likely has higher concurrency than 10, making bug more frequent than local testing shows

## Red Flags Addressed

### Minimal reproduction
**Status**: Script is minimal
- No authentication headers
- No random data generation
- No retry logic
- No sleep statements
- Changes exactly one variable (concurrency)

### Band-aid fix
**Status**: Proper fix implemented
- Used PostgreSQL upsert (INSERT ON CONFLICT DO UPDATE)
- Atomic operation eliminates check-then-act pattern
- No error swallowing - analytics data is correct
- Root cause addressed, not symptom hidden

### Understanding WHY concurrency triggers it
**Explanation**: The check-then-act pattern creates a window between SELECT and INSERT. When two concurrent requests both SELECT and find no row, both attempt INSERT. First succeeds, second fails with unique constraint violation. The upsert closes this window by making existence check and insert/update a single atomic operation - database serializes concurrent upserts internally, preventing the race.

## Key Takeaways

1. **Concurrency is a variable**: Must test with concurrent requests, not just single sequential requests
2. **Check-then-act is dangerous**: Always use atomic operations for concurrent access patterns
3. **Audit codebase for pattern**: SELECT-then-INSERT appears in many places - all are potential race conditions
4. **Concurrency level matters**: 10 concurrent requests provides reliable reproduction without overwhelming system
5. **Production has higher concurrency**: If bug triggers with 10 locally, it definitely triggers in production under real load
