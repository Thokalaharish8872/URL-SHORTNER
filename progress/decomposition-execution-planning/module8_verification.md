# Module 8 Verification

## User Journey Walkthrough: Employee Booking Flow

**Step 1: User searches for provider**
- Component: Frontend → GET /api/providers (Provider Service)
- Handoff: Frontend sends HTTP GET request to /api/providers
- Data crossing boundary: Request headers (JWT token), Query parameters (none)
- Data format: Request: standard HTTP GET. Response: JSON array of provider objects with provider_id (UUID v4), name (string), category (string), rating (decimal)
- Error handling: If provider service down, returns 500 with error message

**Step 2: User views provider profile**
- Component: Frontend → GET /api/providers/:id (Provider Service)
- Handoff: Frontend sends HTTP GET request to /api/providers/{provider_id}
- Data crossing boundary: provider_id (UUID v4 string) in URL path
- Data format: Request: provider_id in URL path. Response: JSON object with provider details, services array, available_slots array
- Data shape: available_slots contains slot_id (UUID v4), start_time (ISO 8601 string), end_time (ISO 8601 string)
- Error handling: Invalid provider_id returns 404 with error message

**Step 3: User selects time slot**
- Component: Frontend (client-side state)
- Handoff: No network handoff - frontend stores selected slot_id in local state
- Data crossing boundary: None
- Data format: slot_id stored as UUID v4 string in JavaScript variable

**Step 4: User books the slot**
- Component: Frontend → POST /api/bookings (Booking Service)
- Handoff: Frontend sends HTTP POST request to /api/bookings
- Data crossing boundary: Request body with provider_id (UUID v4), service_id (UUID v4), slot_id (UUID v4), JWT token in Authorization header
- Data format: Request: JSON body with UUID fields. Response: JSON with booking_id (UUID v4), status (string), created_at (ISO 8601 string)
- Middleware: Booking service extracts role from JWT, validates employee role (can only book for self), validates slot status='available'
- Database transaction: Creates booking record, updates time_slots.status to 'booked' atomically

**Step 5: Booking confirmation**
- Component: POST /api/bookings → Database → Frontend
- Handoff: Booking service returns response to frontend
- Data crossing boundary: Response body with booking details
- Data format: JSON with booking_id, provider_id, service_id, slot_id, status='confirmed', created_at (ISO 8601)
- Error handling: If slot no longer available (race condition), returns 409 with error message

**Step 6: User sees confirmation**
- Component: Frontend (UI display)
- Handoff: No network handoff - frontend displays response from step 5
- Data crossing boundary: None
- Data format: UI displays booking_id, provider name, time slot, status

## Requirements Traceability Audit

**Deferred Requirements (8 total):**

1. **Cancellation policy (24 hours advance notice, full refund)**
   - Status: Deferred
   - When will be built: Week after demo
   - Is it on a ticket: Will be added to post-demo backlog
   - Reason for deferral: Not required for Meridian demo focus on role-based booking

2. **Provider can set their own availability**
   - Status: Deferred
   - When will be built: Week after demo (Provider Self-Service Slice 3)
   - Is it on a ticket: Slice 3 tickets deferred
   - Reason for deferral: Meridian is booking services, not providing them

3. **Provider can view their bookings**
   - Status: Deferred
   - When will be built: Week after demo (Provider Dashboard)
   - Is it on a ticket: Provider Dashboard CUT from 6-day scope
   - Reason for deferral: Not required for Meridian demo

4. **Provider can manage their profile**
   - Status: Deferred
   - When will be built: Week after demo (Provider Self-Service)
   - Is it on a ticket: Slice 3 tickets deferred
   - Reason for deferral: Not required for Meridian demo

5. **Search/filter providers by category**
   - Status: Deferred
   - When will be built: Week after demo
   - Is it on a ticket: Search/Filtering CUT from 6-day scope
   - Reason for deferral: Basic listing with 3 seeded providers sufficient for demo

6. **Email notifications for bookings**
   - Status: Deferred
   - When will be built: Week after demo
   - Is it on a ticket: Email Notifications CUT from 6-day scope
   - Reason for deferral: On-screen confirmation sufficient for demo

7. **Real-time availability with conflict detection**
   - Status: Deferred
   - When will be built: Week after demo (Real-Time Availability Slice 5)
   - Is it on a ticket: Slice 5 tickets deferred
   - Reason for deferral: Static seeded slots sufficient for demo with role-based access

8. **Payment processing with Stripe**
   - Status: Deferred (Simulated)
   - When will be built: Week after demo
   - Is it on a ticket: Payment Processing CUT from SHOULD SHIP to CUT
   - Reason for deferral: Timeline compression - cut to make room for role-based access complexity. Will use simulated payment for demo.

**Simplified Requirements (2 total):**

1. **Payment processing**
   - Original: Full Stripe integration with live payments
   - Simplified: Simulated payment confirmation for demo
   - Conscious decision: Yes - explicitly cut from SHOULD SHIP to CUT in Module 7 to accommodate role-based access scope growth
   - Scope erosion: No - deliberate tradeoff documented in impact statement

2. **Cancellation policy**
   - Original: 24-hour advance notice, full refund, partial refund for less notice
   - Simplified: Not implemented in 6-day scope
   - Conscious decision: Yes - deferred as not required for Meridian demo focus
   - Scope erosion: No - explicit deferral decision

**Lost Requirements (0 total):**
- No requirements were lost. All Module 1 requirements are either built, simplified with conscious decision, or deferred with explicit timeline.

## Contract Validation

**Contract: POST /api/bookings (Sender: Frontend/Booking Service) → Database (Receiver: Time Slots Table)**

**Sender output (from Contract 4 and Ticket 4):**
- Request body: { provider_id: uuid (v4), service_id: uuid (v4), slot_id: uuid (v4) }
- Additional for role-based access: booked_for_name: string, booked_for_email: string (when role=manager or department_head)
- JWT token: Bearer <token> with payload { user_id: uuid, role: enum, department_id: uuid }

**Receiver expected input (Database schema):**
- bookings table: id (uuid v4), provider_id (uuid v4), service_id (uuid v4), slot_id (uuid v4), user_id (uuid v4), status (enum), booked_for_name (string, nullable), booked_for_email (string, nullable)
- time_slots table: id (uuid v4), service_id (uuid v4), start_time (ISO 8601), end_time (ISO 8601), status (enum)

**Validation:**
- provider_id: Sender sends UUID v4 string, Receiver expects UUID v4 → MATCH
- service_id: Sender sends UUID v4 string, Receiver expects UUID v4 → MATCH
- slot_id: Sender sends UUID v4 string, Receiver expects UUID v4 → MATCH
- booked_for_name: Sender sends string, Receiver expects string (nullable) → MATCH
- booked_for_email: Sender sends string, Receiver expects string (nullable) → MATCH
- status: Sender expects 'confirmed'/'failed' in response, Receiver stores enum values → MATCH
- start_time/end_time: Receiver stores ISO 8601 strings, Sender doesn't send these (they're read from database) → MATCH (no conflict)

**Contract: JWT Token Structure (Sender: Auth Service) → All Authenticated Endpoints (Receiver: Booking Service, Bookings Service)**

**Sender output (from Contract 6 and Module 7):**
- JWT token payload: { user_id: uuid v4, email: string, role: enum (employee/manager/department_head), department_id: uuid v4, company_name: string }
- Token format: Bearer <token> in Authorization header

**Receiver expected input (from Module 7 contracts):**
- Middleware extracts: role (enum), department_id (uuid v4), user_id (uuid v4)
- Role values: employee, manager, department_head

**Validation:**
- role: Sender sends enum (employee/manager/department_head), Receiver expects same enum values → MATCH
- department_id: Sender sends UUID v4, Receiver expects UUID v4 → MATCH
- user_id: Sender sends UUID v4, Receiver expects UUID v4 → MATCH
- Token format: Bearer <token> → MATCH

**Conclusion:** All interface contracts match exactly. No field name mismatches, no type mismatches, no enum value mismatches, no date format mismatches.
