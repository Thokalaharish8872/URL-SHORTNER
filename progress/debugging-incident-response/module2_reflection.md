# Module 2 Reflection: Log Literacy

## Comprehension Questions

### 1. What core problem does this module solve in reading logs like a story?
The module solves the problem of extracting signal from noise in structured logs. It teaches reading logs as a timeline - following request IDs from start to finish, understanding log levels as a triage system (FATAL/ERROR = critical, WARN = concerning, INFO = baseline, DEBUG = detailed), and identifying anomalies like missing request IDs, embedded malicious content, or timezone mismatches. The core skill is treating logs as a narrative where each log line is a sentence in the service's life story.

### 2. Which decision in this module has the biggest impact, and why?
The log strategy decision (verbose vs minimal by default) has the biggest impact. Choosing minimal logging (WARN and above) saves significant cost ($1,000/day at 10K req/sec) and reduces cognitive overload, but risks missing bugs that only log at INFO level. This decision frames how observability is implemented - whether you have all data upfront (but must filter through noise) or you collect targeted data and increase verbosity on-demand. The tradeoff is genuine: cost and searchability vs. risk of blind spots.

### 3. What evidence proves the implementation works end-to-end?
For the timezone fix: Create a link near midnight UTC, check log timestamp (UTC) and database timestamp (should match in UTC), query for links created "today" using UTC midnight - the link should resolve immediately without 404. For the log injection fix: Submit URL with newline and injected JSON, verify log output shows entire malicious URL as single string value in one log line, not as separate forged entry. Both fixes demonstrate the vulnerabilities are resolved.

## Mini Practical Task

### STEP 4 Verification: Reading Logs Like a Story

**Task**: Reconstruct request r-004 timeline from structured logs

**Log excerpt**:
```json
{"ts":"2025-01-15T14:00:08.200Z","level":"info","req_id":"r-004","msg":"request received","method":"POST","path":"/links","status":null}
{"ts":"2025-01-15T14:00:08.890Z","level":"warn","req_id":"r-004","msg":"slow db write","short_code":"pL3nR","duration_ms":680}
{"ts":"2025-01-15T14:00:08.900Z","level":"info","req_id":"r-004","msg":"response sent","status":201,"duration_ms":700}
```

**Reconstructed timeline**:
- 14:00:08.200Z - Request received (POST /links)
- 14:00:08.890Z - Slow database write warning (680ms into request)
- 14:00:08.900Z - Response sent (status 201 Created, total duration 700ms)

**What happened**: User submitted a POST request to create a link. The database write was slow (680ms), triggering a WARN level log. The link was successfully created with short_code pL3nR. The service responded with 201 Created status. Total request duration was 700ms.

**Missing log lines** (would improve story):
- Link creation completion confirmation
- URL validation result
- Short code generation step
- Cache operation (if any)

## Risk and Mitigation

### Risk
**Log injection vulnerability** - User input can forge log entries by embedding control characters, allowing attackers to spoof privileged actions and corrupt audit trails.

### Mitigation
**Input sanitization before logging** - Remove control characters from user-supplied data, use structured logging with proper JSON encoding, validate input at API boundary. This prevents malicious content from breaking log structure or appearing as separate log entries.

## Key Takeaways

1. **Logs are a narrative** - Read them as a timeline following request IDs from start to finish
2. **Log levels are triage** - Use them to control volume and prioritize investigation (FATAL/ERROR = critical, INFO = baseline)
3. **Timezone bugs are dangerous** - Always store UTC, convert to local time only at display layer
4. **Logs can be forged** - User input must be sanitized before logging to prevent injection attacks
5. **Minimal logging saves cost** - But requires ability to increase verbosity on-demand for investigation
