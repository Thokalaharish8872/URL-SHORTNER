# Task 3 BREAK Analysis: Convention Violation

## The Violation

**Task 3: Create Team CRUD API Endpoints** has an error handling convention violation.

## Existing Codebase Pattern
From `api/app/main.py`, error responses follow this format:
```json
{
  "detail": "Error message here"
}
```

Status codes used:
- 422 for validation errors
- 404 for not found
- 500 for unexpected errors

## Agent Output (Simulated Violation)
The agent produced error responses like this:
```json
{
  "status": "error",
  "message": "Team name is required.",
  "statusCode": 400
}
```

## The Difference
- **Structure**: Existing uses `{"detail": "message"}` while agent uses `{"status", "message", "statusCode"}`
- **Status code**: Existing uses 422 for validation errors while agent uses 400
- **Field names**: Existing uses `detail` while agent uses `message`

## Why This Happened
The context package for Task 3 included `api/app/main.py` to show route registration pattern, but did NOT include a specific example of an existing error response. The system-level context document specified the error format as:
```
Error responses follow this format:
{
  "detail": "Error message here"
}
```

However, this was a general description, not a concrete code example. The agent, when implementing error handling in the TeamService or route handlers, defaulted to a "reasonable" error format that didn't match the existing pattern.

## Impact
If a client application is parsing error responses from the API, it now needs to handle two different formats depending on which endpoint it calls. This creates inconsistency and will confuse every developer who consumes the API. Clients expecting `{"detail": "message"}` from existing endpoints will break when calling the new Team endpoints.

## Root Cause
Missing concrete example in context package. The system-level context described the format textually but didn't show an actual code snippet from `api/app/main.py` demonstrating how errors are returned. The agent had to infer the pattern and chose a different but "reasonable" format.

## Fix
Add a concrete example to Task 3's context bundle showing an existing error response from `api/app/main.py`:
```python
# Example from existing endpoint
raise HTTPException(status_code=404, detail="Link not found")
```

This would make the pattern explicit and prevent the agent from inventing a different format.
