# Module 2 Fix: Log Injection Vulnerability

## Root Cause
User-supplied input (URL field) was written directly to log output without sanitization. The URL contained a newline character (`\n`) followed by a crafted JSON string that appeared as a separate log entry.

## Evidence of Forgery

The "admin login successful" log line is fake because:
1. **No request received line**: Request ID r-102 has no corresponding "request received" entry - every real request starts with this
2. **Embedded in another request**: The fake log appears inside r-101's timeline between "link created" and "response sent"
3. **Timestamp anomaly**: The fake log timestamp (15:42:03.500Z) is between r-101's processing steps, suspiciously placed
4. **Malformed JSON**: The log line is not valid JSON - it's two JSON objects concatenated

## Attack Vector

**Actual URL submitted by Bob**:
```
https://normal-url.com\n{"ts":"2025-01-15T15:42:03.500Z","level":"info","req_id":"r-102","msg":"admin login successful","user":"admin","ip":"10.0.0.1"}
```

This is **one URL** with a forged log line embedded inside it. The newline character breaks the log entry, making the injected JSON appear as a separate log line.

## Fix: Sanitize User Input Before Logging

### 1. Remove Control Characters
```python
import re

def sanitize_for_logging(value: str) -> str:
    """Remove control characters from user input before logging."""
    if isinstance(value, str):
        # Remove ASCII control characters (0x00-0x1f) and DEL (0x7f)
        return re.sub(r'[\x00-\x1f\x7f]', '', value)
    return value
```

### 2. Use Structured Logging with Proper JSON Encoding
```python
import json
import logging

logger = logging.getLogger(__name__)

# Instead of:
# logger.info(f"link created with url: {user_url}")  # Vulnerable to injection

# Use structured logging:
logger.info({
    "msg": "link created",
    "short_code": short_code,
    "url": sanitize_for_logging(user_url)  # Sanitized
})
```

### 3. Validate URL Format
```python
from pydantic import HttpUrl

def validate_url(url: str) -> str:
    """Validate and sanitize URL."""
    try:
        # Pydantic validates URL format
        validated = HttpUrl(url)
        # Convert to string and sanitize
        return sanitize_for_logging(str(validated))
    except ValueError:
        raise ValueError("Invalid URL format")
```

### 4. Apply in Link Creation
```python
# In api/app/services.py or main.py
@app.post("/links")
def create_link(link_in: LinkCreate, db: Session = Depends(get_db)):
    # Validate and sanitize URL
    sanitized_url = validate_url(str(link_in.long_url))
    
    # Log with sanitized input
    logger.info({
        "msg": "link created",
        "short_code": code,
        "url": sanitized_url,  # Safe for logging
        "user": current_user_id
    })
    
    # Create link with original (unsanitized) URL for database
    link = Link(code=code, long_url=str(link_in.long_url), ...)
```

## Verification

### Test the Fix
1. Submit a URL with newline and injected JSON:
```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://test.com\n{\"fake\":\"log\"}"}'
```

2. Check the log output:
```json
{
  "msg": "link created",
  "short_code": "abc123",
  "url": "https://test.com{\"fake\":\"log\"}",  # Newline removed
  "user": "user123"
}
```

**Expected result**: The entire malicious URL appears as a single string value within one log line - not as a separate forged entry. The newline character is removed or escaped.

### Test Cases
- **Normal URL**: Should log unchanged
- **URL with newline**: Should remove newline, log as single line
- **URL with control characters**: Should remove all control characters
- **URL with embedded JSON**: Should escape or remove, not parse as separate log entry

## Systemic Prevention

### 1. Use a Structured Logging Library
- Python: `structlog`, `python-json-logger`
- These libraries automatically handle JSON escaping
- They prevent injection by treating user data as string values, not interpolating into log format

### 2. Input Validation Layer
- Validate all user input at the API boundary
- Reject requests with control characters in URL fields
- Use schema validation (Pydantic, JSON Schema)

### 3. Log Field Whitelisting
- Only log specific fields that are known to be safe
- Avoid logging raw request bodies
- Log user input as separate, clearly-labeled fields

### 4. Log Integrity Checks
- Add checksums or signatures to critical log entries
- Monitor for anomalous log patterns (missing request IDs, malformed JSON)
- Implement log ingestion validation

## Key Lessons

1. **Never trust user input in logs**: All user-supplied data must be sanitized before logging
2. **Newline characters are dangerous**: They can break log structure and enable injection
3. **Structured logging is safer**: Proper JSON encoding prevents injection attacks
4. **Validate at the boundary**: Catch malicious input before it reaches logging code
5. **Logs can be forged**: Without proper sanitization, attackers can manipulate what gets written to logs
