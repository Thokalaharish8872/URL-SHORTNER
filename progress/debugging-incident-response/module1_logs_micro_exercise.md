# Module 1 Micro-Exercise: Structured Logs Analysis

## Log Lines Analysis

### Question 1: Which request failed? How do you know?
**Answer**: Request r-003 failed.

**How I know**: The log line shows:
```json
{"ts":"2025-01-15T14:00:05.510Z","level":"error","req_id":"r-003","msg":"link not found","short_code":"nope99","status":404,"duration_ms":10}
```
- `level: "error"` indicates a failure
- `status: 404` confirms the resource was not found
- `msg: "link not found"` describes the specific error

### Question 2: How long did the slowest request take? What might explain the slowness?
**Answer**: The slowest request is r-004 with 700ms duration.

**Explanation for slowness**: The log line shows:
```json
{"ts":"2025-01-15T14:00:08.890Z","level":"warn","req_id":"r-004","msg":"slow db write","short_code":"pL3nR","duration_ms":680}
```
- The "slow db write" warning at 680ms indicates database performance issue
- This is a warning level, not an error - the request succeeded but took longer than expected
- Possible causes: database contention, slow disk I/O, network latency to database, or a complex query

### Question 3: Is there a pattern to the failures, or was it a one-off?
**Answer**: It's a one-off failure with no pattern.

**Evidence**:
- Only one error in the 10 log lines (r-003 with 404)
- The error is a "link not found" - user tried to access a non-existent short code "nope99"
- This is a normal user error (typo or invalid link), not a system failure
- No other errors or warnings that indicate a systemic issue
- The slow request (r-004) succeeded despite being slow

## Key Insights from Structured Logs

### What Structured Logs Provide
- **Request tracking**: Each log has `req_id` to follow the full request lifecycle
- **Timestamps**: Precise timing to measure duration and sequence
- **Context**: Method, path, status, and message in every log line
- **Levels**: ERROR, WARN, INFO to control volume and prioritize investigation

### Log Level Triage
- **FATAL/CRITICAL**: Service is dying - drop everything
- **ERROR**: Something broke for a specific request - investigate
- **WARN**: Something looks off but didn't break - monitor
- **INFO**: Normal operations - baseline story
- **DEBUG**: Detailed internal state - use when investigating

### Production Incident Lesson
The checkout platform story showed that setting log level to WARN caused a critical bug (duplicate charges) to be hidden for 3 weeks. The bug was logged at INFO level but filtered out.

**Lesson**: Be careful about log level configuration in production. Setting it too high can hide critical information that would help you catch bugs early.
