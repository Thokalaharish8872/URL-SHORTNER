# Module 5 Incident Simulation: Auth Bypass Under Pressure

## Scenario
SEV1 incident: Auth bypass in admin API allows unauthenticated requests. 47 short links deleted by attacker. VP of Product needs update for prospect demo. Stakeholders pressuring for reassurance.

## Phase 1: Initial Status Update (Minute 5)
**Message**: "Investigating alert about admin API auth bypass. Confirmed unauthorized requests are reaching admin endpoints. Currently assessing scope and impact. Will update in 10 minutes."

**Key elements**: Acknowledge problem, state what's known, state what's unknown, set expectation for next update.

## Phase 2: VP Interruption (Minute 8)
**VP message**: "Update? The prospect just asked about our security practices. My boss is on a call with the CTO. Can you tell me this is not a real breach?"

**Response**: Cannot lie - this IS a real auth bypass with confirmed data deletion. Must be honest without causing panic.

**Good response**: "Update: Vulnerability confirmed - auth bypass in admin API. Approximately 47 short links deleted. Implementing fix now, expect deploy in 10-15 minutes. Important: public redirect service unaffected. Demo can proceed - it doesn't use admin API. Will confirm when fix deployed."

**What to avoid**: Lying ("it's not really a breach") or over-escalating ("everything's compromised, cancel demo") without evidence.

## Phase 3: Fix Implementation
**Root cause**: Auth middleware checks `if (authHeader)` which is truthy for empty string `""` - bypasses authentication.

**Fix**: Validate header contains non-whitespace content, validate format explicitly, validate token portion is non-empty before JWT verification.

**Node.js fix**:
```javascript
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || typeof authHeader !== 'string' || !authHeader.trim()) {
    return res.status(401).json({ error: 'Authorization required' });
  }
  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return res.status(401).json({ error: 'Invalid authorization format' });
  }
  const token = parts[1];
  if (!token) {
    return res.status(401).json({ error: 'Token missing' });
  }
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

**Verification steps**:
1. `Authorization: ""` → 401
2. `Authorization: " "` → 401
3. `Authorization: Bearer` → 401
4. `Authorization: Bearer <valid-token>` → 200
5. No Authorization header → 401

## Phase 4: Incident Close Message
**Message**: "RESOLVED: Admin API auth bypass patched and deployed. Summary: Vulnerability in auth middleware allowed unauthenticated requests to admin endpoints. Approximately 47 short links deleted. Public redirect service unaffected. Next steps: Checking database backups to recover deleted links, conducting postmortem this week. No customer action required. Will send final summary after data recovery."

## Key Lessons

1. **Communicate first, fix second**: Initial 5-minute update prevents organizational damage
2. **Honesty under pressure**: Cannot minimize SEV1 - stakeholders need accurate information
3. **Defense in depth**: Multiple validation checks, not single conditional
4. **Verify all edge cases**: Test not just happy path but empty strings, whitespace, missing tokens
5. **Close message includes next steps**: Data recovery, postmortem, customer action required
