# Module 6 Break: Rogue Agent Contract Violation

## Scenario

Both agents have finished their tickets. All acceptance criteria pass individually. Agent B's output is shown below. Something is off compared to the contract.

## Contract Reference (from contracts-module-06.md)

**Contract 1 - Shared types:**
- datetime format: ISO 8601 (e.g., "2025-03-15T14:30:00Z")

**Contract 3 - GET /api/providers/:id Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "category": "string",
  "rating": "decimal",
  "description": "text",
  "services": [
    {
      "id": "uuid",
      "name": "string",
      "description": "text",
      "price": "decimal"
    }
  ],
  "available_slots": [
    {
      "id": "uuid",
      "start_time": "ISO 8601 datetime",
      "end_time": "ISO 8601 datetime"
    }
  ]
}
```

## Agent B's Actual Output (GET /api/providers/:id)

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
      "start_time": 1710512400,
      "end_time": 1710516000
    }
  ]
}
```

## Violation Analysis

**Issue found:** Date format mismatch in `available_slots`

**Contract specifies:** `start_time` and `end_time` should be "ISO 8601 datetime" (e.g., "2025-03-15T14:30:00Z")

**Agent B returned:** Unix timestamps (integers: 1710512400, 1710516000)

**Why this is a problem:**
- The frontend consuming this API expects string dates for display
- The booking agent expects ISO 8601 strings when parsing slot selection
- Date comparison logic (`slot.start_time > NOW()`) will fail with integer timestamps if the database expects timestamps
- This is a contract violation even though the code works in isolation

**Root cause:** Agent B used Unix timestamps "because it is more efficient for database storage" without considering the interface contract requirement for ISO 8601 format.

**Impact:** When Agent A (frontend) tries to display the date to the user, it will show "1710512400" instead of "March 15, 2025 at 2:00 PM". When Agent B (booking) tries to parse the slot selection, it may fail or produce incorrect dates.

## Fix Required

Agent B must convert Unix timestamps to ISO 8601 strings in the API response, even if storing as integers in the database. The contract specifies the output format, not the storage format.
