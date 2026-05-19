# Module 6 Fix: Contract Violation Resolution

## Decision: Fix the Rogue Agent

**Choice:** Fix Agent B's output to match the original contract.

**Reasoning:**
- ISO 8601 is the industry standard for API datetime formats
- Human-readable and timezone-aware
- Better for debugging and logging
- Unix timestamps require timezone context (are they UTC? local?)
- The contract was correct; the agent deviated without justification
- Updating the contract would require fixing the frontend agent too, creating more work

## Production Impact

**Symptom:** The frontend displays "1710512400" instead of "March 15, 2025 at 2:00 PM." Users see raw integers for time slots, making the app unusable.

**When someone notices:** Immediately upon first user booking. The UI breaks as soon as a user tries to view available slots.

**Worse case:** If the frontend has date comparison logic (e.g., "show only future slots"), the comparison might fail silently. Users might see slots from 1970 or no slots at all, depending on how the frontend handles the integer.

## Fix Execution

**Action:** Update Agent B's GET /api/providers/:id endpoint to convert Unix timestamps to ISO 8601 strings before returning the response.

**Updated Agent B Output:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Mike's Plumbing",
  "category": "plumbing",
  "rating": 4.5,
  "description": "Professional plumbing services",
  "services": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Basic Plumbing",
      "description": "General plumbing repairs",
      "price": 75.00
    }
  ],
  "available_slots": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "start_time": "2025-03-15T14:00:00Z",
      "end_time": "2025-03-15T15:00:00Z"
    }
  ]
}
```

**Re-verify Sarah scenario:**
- Sarah opens app → GET /api/providers returns provider list ✓
- Sarah clicks Mike → GET /api/providers/:id returns slots with ISO 8601 dates ✓
- Sarah selects Tuesday 2pm → POST /api/bookings accepts slot_id (UUID) ✓
- No mismatches remain

## Prevention Strategies

**1. Shared Type Definitions**
- Create a shared types file (e.g., `types.ts` or `shared-types.json`) that both agents import
- Single source of truth for all data shapes
- Change in one place propagates to both agents

**2. Contract Tests (Automated)**
- Write tests that validate API responses against the contract schema
- Use tools like JSON Schema validation or OpenAPI specification validation
- Run in CI pipeline before merge

**3. Pre-Merge Checklist**
- Add checklist item: "Verify response shapes match contract"
- Manual diff between actual output and contract before merging
- Required for all parallel work integration points

**4. Code Generation from Contract**
- Use OpenAPI spec to generate server stubs and client types
- Contract is the source of truth
- Agent implements generated interfaces, cannot deviate

**5. Contract-First Development**
- Write contract before any code
- Both agents implement against the same contract
- Contract review becomes part of the planning phase

**Chosen approach for this project:** Contract tests + pre-merge checklist. Contract tests catch violations automatically in CI. Pre-merge checklist provides human verification for edge cases tests might miss.
