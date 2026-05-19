# Module 6 Verification: Contract and Output Verification

## Contract Verification

### 1. ID Type Specification
**Location:** Contract 1 "Database Schema" section
- provider_id: uuid (v4)
- service_id: uuid (v4)
- slot_id: uuid (v4)
- user_id: uuid (v4)
- booking_id: uuid (v4)

All ID fields are explicitly specified as UUID v4 format across all contracts.

### 2. Error Format Specification
**Location:** Contract 2, Contract 3, Contract 4
- All error responses follow format: `{ "error": "<message>" }`
- Specific error codes: 400 for invalid input, 404 for not found, 409 for conflicts
- Example from Contract 4: "POST /api/bookings must validate slot exists and status='available' before booking"

### 3. Datetime Format Specification
**Location:** Contract 1 "Shared types" section
- datetime format: ISO 8601 (e.g., "2025-03-15T14:30:00Z")
- Database schema uses: timestamp with time zone
- All contracts specify ISO 8601 for API responses

### 4. Fields Produced but Not Consumed
**Location:** Contract 5 "POST /api/bookings <-> Future Tickets"
- POST /api/bookings returns: booking_id, provider_id, service_id, slot_id, user_id, status, created_at
- Slice 1 bookings are anonymous (user_id is nullable)
- Future tickets (My Bookings) will consume by user_id, but must handle NULL case for Slice 1 bookings
- Reason: Slice 1 doesn't have auth, so user_id is nullable. This is intentional - allows anonymous bookings in first slice, authenticated bookings in later slices.

---

## End-to-End Scenario: Sarah Books Mike's Plumbing Service

**Scenario:** Sarah opens the app, browses providers, finds Mike (plumbing), sees his available slots, picks Tuesday at 2pm, and confirms the booking.

### Trace Through Agents

**Step 1: Sarah browses providers**
- **Agent:** Ticket 2 (GET /api/providers)
- **Response:**
  ```json
  {
    "providers": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Mike's Plumbing",
        "category": "plumbing",
        "rating": 4.5
      }
    ]
  }
  ```

**Step 2: Sarah clicks Mike to see details**
- **Agent:** Ticket 3 (GET /api/providers/:id)
- **Request:** GET /api/providers/550e8400-e29b-41d4-a716-446655440000
- **Response:**
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
        "start_time": "2025-03-18T14:00:00Z",
        "end_time": "2025-03-18T15:00:00Z"
      }
    ]
  }
  ```

**Step 3: Sarah selects Tuesday 2pm slot and clicks confirm**
- **Agent:** Ticket 4 (POST /api/bookings)
- **Request:**
  ```json
  {
    "provider_id": "550e8400-e29b-41d4-a716-446655440000",
    "service_id": "660e8400-e29b-41d4-a716-446655440001",
    "slot_id": "770e8400-e29b-41d4-a716-446655440002"
  }
  ```
- **Response:**
  ```json
  {
    "booking_id": "880e8400-e29b-41d4-a716-446655440003",
    "provider_id": "550e8400-e29b-41d4-a716-446655440000",
    "service_id": "660e8400-e29b-41d4-a716-446655440001",
    "slot_id": "770e8400-e29b-41d4-a716-446655440002",
    "status": "confirmed",
    "created_at": "2025-03-15T10:30:00Z"
  }
  ```

### Contract Compliance Check

**Does Agent A's availability response match Agent B's booking expectations?**
- Agent A returns slot_id as UUID v4: "770e8400-e29b-41d4-a716-446655440002"
- Agent B expects slot_id as UUID v4 in request body
- **YES** - formats match, both use UUID v4

**What happens if slot was booked by someone else between Sarah seeing it and clicking confirm?**
- **Agent:** Ticket 4 (POST /api/bookings)
- **Contract coverage:** Contract 4 specifies "POST /api/bookings must validate slot exists and status='available' before booking"
- **Behavior:** Agent B checks time_slots table for slot_id, verifies status='available'. If status='booked' (someone else booked it), returns 409 with error "slot unavailable"
- **Handling:** Frontend shows error to Sarah: "This slot is no longer available. Please select another time."

### Red Flags Check

- ✅ Contracts written before "agent launch" (contracts created in BUILD step)
- ✅ Contracts are specific to my tickets (not copy-pasted template - includes my actual endpoints, data structures)
- ✅ Output shapes match contract specifications (all UUIDs as v4, ISO 8601 timestamps, decimal formats)
