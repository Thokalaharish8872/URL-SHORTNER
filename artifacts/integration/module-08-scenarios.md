# Module 8: End-to-End Scenario Testing

## Phase 3: End-to-End Scenario Testing

### Scenario 1: Happy Path Booking Flow (Employee)

**Steps and Component Handoffs:**

1. **User searches for provider**
   - Component: Frontend → GET /api/providers
   - Handoff: Frontend sends request, API returns provider list
   - Data check: Provider list includes provider_id, name, category, rating in correct formats

2. **User views provider profile**
   - Component: Frontend → GET /api/providers/:id
   - Handoff: Frontend sends provider_id from step 1, API returns provider details
   - Data check: Response includes services array and available_slots with slot_id, start_time, end_time

3. **User selects time slot**
   - Component: Frontend (stores selected slot_id)
   - Handoff: Frontend stores slot_id locally
   - Data check: slot_id is UUID v4 format

4. **User books the slot**
   - Component: Frontend → POST /api/bookings
   - Handoff: Frontend sends provider_id, service_id, slot_id with JWT token
   - Data check: API validates JWT role=employee, validates slot status='available', creates booking

5. **Booking is confirmed**
   - Component: POST /api/bookings → Database → Frontend
   - Handoff: API returns booking_id, status='confirmed', created_at (ISO 8601)
   - Data check: Response includes booking_id (UUID v4), status='confirmed'

6. **User receives confirmation**
   - Component: Frontend displays booking confirmation
   - Handoff: Frontend shows booking details from step 5
   - Data check: Confirmation shows booking_id, provider, time slot, status

**Result:** PASSED - All handoffs successful, data formats match contracts

---

### Scenario 2: Manager Booking for Employee (Delegation)

**Steps and Component Handoffs:**

1. **Manager logs in**
   - Component: Frontend → POST /api/auth/login
   - Handoff: Frontend sends credentials, API returns JWT with role=manager, department_id
   - Data check: JWT payload includes role='manager'

2. **Manager searches for provider**
   - Component: Frontend → GET /api/providers
   - Handoff: Same as Scenario 1
   - Data check: Provider list returned correctly

3. **Manager views provider profile**
   - Component: Frontend → GET /api/providers/:id
   - Handoff: Same as Scenario 1
   - Data check: Provider details with slots returned correctly

4. **Manager selects time slot**
   - Component: Frontend (stores selected slot_id)
   - Handoff: Same as Scenario 1
   - Data check: slot_id stored correctly

5. **Manager fills delegation fields**
   - Component: Frontend shows "Who is this booking for?" (visible because role=manager)
   - Handoff: Frontend captures booked_for_name, booked_for_email
   - Data check: Delegation fields captured

6. **Manager submits booking**
   - Component: Frontend → POST /api/bookings
   - Handoff: Frontend sends provider_id, slot_id, booked_for_name, booked_for_email with JWT
   - Data check: Middleware extracts role=manager from JWT, allows delegation

7. **Booking created with delegation**
   - Component: POST /api/bookings → Database
   - Handoff: API saves booking with booked_for_name, booked_for_email
   - Data check: Database record includes delegation fields

8. **Manager sees booking in My Bookings**
   - Component: Frontend → GET /api/bookings
   - Handoff: API returns all company bookings (because role=manager)
   - Data check: Response includes delegated booking with booked_for_name

**Result:** PASSED - Role-based access allows delegation, data propagated correctly

---

### Scenario 3: Department Head Booking Scope Limitation

**Steps and Component Handoffs:**

1. **Department head logs in**
   - Component: Frontend → POST /api/auth/login
   - Handoff: API returns JWT with role=department_head, department_id=deptA
   - Data check: JWT payload includes role='department_head', department_id='deptA'

2. **Department head searches for provider**
   - Component: Frontend → GET /api/providers
   - Handoff: Same as previous scenarios
   - Data check: Provider list returned correctly

3. **Department head attempts to book for employee in different department**
   - Component: Frontend → POST /api/bookings
   - Handoff: Frontend sends booked_for_email for user in deptB
   - Data check: Middleware extracts role=department_head, queries booked_for user's department_id

4. **Booking rejected**
   - Component: POST /api/bookings middleware
   - Handoff: Middleware checks current_user.department_id != booked_for_user.department_id
   - Data check: API returns 403 Forbidden with error message

5. **Department head books for employee in same department**
   - Component: Frontend → POST /api/bookings
   - Handoff: Frontend sends booked_for_email for user in deptA
   - Data check: Middleware validates departments match, allows booking

6. **Booking created**
   - Component: POST /api/bookings → Database
   - Handoff: API saves booking with delegation fields
   - Data check: Database record includes delegation fields

7. **Department head sees only department bookings**
   - Component: Frontend → GET /api/bookings
   - Handoff: API returns only deptA bookings (because role=department_head)
   - Data check: Response does not include bookings from other departments

**Result:** PASSED - Department head scope limitation working correctly

---

### Scenario 4: Concurrent Booking Conflict (Edge Case)

**Steps and Component Handoffs:**

1. **User A and User B both get same slot_id**
   - Component: Frontend → GET /api/providers/:id
   - Handoff: Both users call API, receive same available_slots
   - Data check: Both users see slot_id=slot123 as available

2. **User A submits booking first**
   - Component: Frontend A → POST /api/bookings
   - Handoff: API checks slot status='available', updates to 'booked' in transaction
   - Data check: Booking created, slot status updated atomically

3. **User B submits booking second**
   - Component: Frontend B → POST /api/bookings
   - Handoff: API checks slot status='booked', rejects booking
   - Data check: API returns 409 Conflict with error "slot not available"

4. **User A sees their booking**
   - Component: Frontend A → GET /api/bookings
   - Handoff: API returns User A's booking
   - Data check: Booking confirmed

5. **User B sees conflict error**
   - Component: Frontend B displays error
   - Handoff: Frontend shows 409 error message
   - Data check: No corrupt booking created for User B

**Result:** PASSED - Concurrent access handled correctly, no data corruption
