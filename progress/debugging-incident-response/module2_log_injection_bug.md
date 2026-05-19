# Module 2 Break: Log Injection Attack

## Suspicious Log Excerpt

```
{"ts":"2025-01-15T15:42:01.200Z","level":"info","req_id":"r-100","msg":"request received","method":"POST","path":"/links","user":"alice"}
{"ts":"2025-01-15T15:42:01.250Z","level":"info":"req_id":"r-100","msg":"link created","short_code":"mN7pQ","url":"https://legit-site.com"}
{"ts":"2025-01-15T15:42:01.255Z","level":"info","req_id":"r-100","msg":"response sent","status":201,"duration_ms":55}
{"ts":"2025-01-15T15:42:03.400Z","level":"info","req_id":"r-101","msg":"request received","method":"POST","path":"/links","user":"bob"}
{"ts":"2025-01-15T15:42:03.410Z","level":"info","req_id":"r-101","msg":"link created","short_code":"qR2wX","url":"https://normal-url.com\n{\"ts\":\"2025-01-15T15:42:03.500Z\",\"level\":\"info\",\"req_id\":\"r-102\",\"msg\":\"admin login successful\",\"user\":\"admin\",\"ip\":\"10.0.0.1\"}"}
{"ts":"2025-01-15T15:42:03.420Z","level":"info","req_id":"r-101","msg":"response sent","status":201,"duration_ms":20}
```

## Analysis

### What's Wrong
Line 5 contains a **log injection attack**. The `url` field includes:
```
"https://normal-url.com\n{\"ts\":\"2025-01-15T15:42:03.500Z\",\"level\":\"info\",\"req_id\":\"r-102\",\"msg\":\"admin login successful\",\"user\":\"admin\",\"ip\":\"10.0.0.1\"}"
```

### Evidence in the Log Itself

1. **Embedded newline character**: The URL contains `\n` (newline) which breaks the JSON structure
2. **Embedded JSON**: After the newline, there's a complete JSON object mimicking an admin login log
3. **Malformed JSON**: The log line is not valid JSON - it's two JSON objects concatenated
4. **Suspicious timing**: The "admin login" timestamp (15:42:03.500Z) is AFTER the link creation timestamp (15:42:03.410Z) but appears in the same log line
5. **No request received for r-102**: There's no "request received" log for request ID r-102, yet it shows "admin login successful"

### What Happened

**This is a log injection attack**, not a real admin login.

**Attack scenario**:
1. User "bob" submitted a URL containing a newline character followed by a fake JSON log entry
2. The logging system did not sanitize the URL before logging
3. The logger wrote the URL verbatim, including the newline and fake log
4. When reading logs, it appears as if an admin logged in, but it's actually part of the URL field from bob's request

### Why This Matters

**Log injection vulnerabilities allow attackers to**:
- Spoof log entries to make it look like privileged actions occurred
- Hide malicious activity by drowning it in fake logs
- Confuse log analysis and incident response
- Bypass security monitoring that relies on log patterns

### Real-World Impact

If this went unnoticed:
- An attacker could make it look like "admin" performed actions they actually performed
- Security teams investigating logs would see fake admin activity
- Audit trails would be corrupted
- Forensic analysis would be compromised

### Root Cause

The logging system does not:
1. Sanitize user input before logging (URLs contain `\n` and JSON)
2. Validate that log fields don't contain control characters
3. Escape or quote strings properly
4. Use structured logging libraries that handle escaping automatically

### Fix

**Immediate fixes**:
1. Sanitize all user input before logging (remove newlines, control characters)
2. Use a structured logging library that handles JSON escaping
3. Validate that URL fields contain valid URLs only
4. Add input validation to reject URLs with control characters

**Example fix**:
```python
import re

def sanitize_for_logging(value):
    # Remove control characters
    if isinstance(value, str):
        return re.sub(r'[\x00-\x1f\x7f]', '', value)
    return value

# When logging
logger.info({
    "msg": "link created",
    "url": sanitize_for_logging(user_provided_url)
})
```

### Key Insight

**Logs can lie if user input is not sanitized before logging.** This is a form of log injection - a security vulnerability where attackers can manipulate what gets written to logs by embedding special characters in their input.

This means every log line that contains user input (URLs, user agents, referrers, request bodies) could potentially be forged if not properly sanitized.
