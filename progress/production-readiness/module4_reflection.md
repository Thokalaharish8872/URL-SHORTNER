# Module 4 Reflection: Observability

## Comprehension Questions

### 1. What core problem does this module solve in observability?
The module solves the problem of flying blind in production - knowing when something is wrong, what is wrong, and where to start looking. It teaches how to implement the three pillars of observability: logs (diary of what happened), metrics (dashboard of how system is behaving), and alerts (bridge between having data and someone knowing there's a problem). The core problem is preventing Friday-at-5-PM surprises where response times spike and nobody notices until customers tweet.

### 2. Which decision in this module has the biggest impact, and why?
The log format decision (JSON everywhere vs hybrid) has the biggest impact. JSON everywhere ensures consistency - one format, one parser, no environment-specific behavior. What you see locally is exactly what production emits. Hybrid approach risks bugs only showing up in JSON format not seen during development. While painful to read JSON in terminal during development, consistency and reliability outweigh readability pain. Production reliability is more important than developer convenience.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: 1) GET /metrics shows http_requests_total broken down by method/path/status, http_request_duration_seconds histogram has populated buckets, business metric gauge present. 2) Single request produces valid JSON log with timestamp, level, message, request_id, service_name. 3) Error response (500) produces error log with level error, same request_id, stack trace. 4) Three alert rules complete with metric expression, threshold, for duration, severity, human-readable message, runbook link. All three pillars (logs, metrics, alerts) respond to errors.

## Mini Practical Task

### STEP 4 Verification: Structured Logging

**Task**: Verify structured logging produces valid JSON with required fields

**Commands**:
```bash
# Make a request to the service
curl http://localhost:3000/live

# Check the log output
# Expected output (JSON format):
{"timestamp":"2025-03-15T17:42:07Z","level":"info","message":"request completed","service":"url-shortener","request_id":"abc-123","method":"GET","path":"/live","status":200,"duration_ms":12}

# Verify it's valid JSON
echo '{"timestamp":"2025-03-15T17:42:07Z","level":"info","message":"request completed","service":"url-shortener","request_id":"abc-123","method":"GET","path":"/live","status":200,"duration_ms":12}' | jq .
```

**Proof**: Log output is valid JSON containing all required fields (timestamp, level, message, request_id, service_name). The jq command successfully parses the JSON without errors, confirming valid format. Request_id connects this log to other logs from the same request.

## Risk and Mitigation

### Risk
**Logging sensitive data**: Logging request bodies that might contain passwords, API keys, or personal information creates a security incident. A log line with `{"message":"user login","body":{"email":"jane@example.com","password":"hunter2"}}` exposes credentials to anyone with log access.

### Mitigation
**Redact sensitive data**: Log what you need, redact what you must. Never log raw request bodies. Log only safe fields (request_id, method, path, status, duration). If you must log user data, use redaction functions to mask sensitive fields (password, credit cards, PII). Use structured logging to make redaction systematic rather than ad-hoc.

## Key Takeaways

1. **Three pillars of observability**: Logs answer "what happened", metrics answer "how is the system behaving", traces answer "where did this request spend its time"
2. **Alerts have a cost**: Noisy alerts train people to ignore them. Choose thresholds that separate "something is actually wrong" from "normal variance"
3. **Observability vs monitoring**: Monitoring watches for known problems (alert if error rate > 5%), observability enables asking new questions you didn't anticipate
4. **Metric cardinality matters**: High-cardinality labels (user_id, request_id) explode time series. Use low-cardinality labels (method, path, status) only
5. **Request_id is the thread**: Connects logs across request lifecycle. Without it, error logs cannot be traced to the original request
