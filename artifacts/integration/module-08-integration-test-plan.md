# Module 8: Integration Test Plan

## Phase 5: Integration Test Plan

### Test 1: Booking Creation Propagates to Provider Dashboard

**Name:** Booking creation updates slot status and is visible in bookings endpoint

**Components involved:**
- POST /api/bookings (booking service)
- Database (time_slots table, bookings table)
- GET /api/bookings (bookings retrieval service)

**Setup:**
- User with role=manager logged in (JWT token)
- Provider with available slot seeded in database
- Slot status='available' before test

**Steps:**
1. Call POST /api/auth/login to get JWT token with role=manager
2. Call GET /api/providers/:id to get available slot_id
3. Call POST /api/bookings with provider_id, slot_id, booked_for_name, booked_for_email, JWT token
4. Query database directly: SELECT status FROM time_slots WHERE slot_id = [slot_id]
5. Call GET /api/bookings with JWT token

**Expected result:**
- Step 3: Returns 201 with booking_id, status='confirmed'
- Step 4: Database shows slot status='booked' (atomic transaction verified)
- Step 5: Response includes the newly created booking with delegation info

**Contract points validated:**
- POST /api/bookings request/response shape
- Database atomic transaction (booking + slot update)
- JWT role validation allows manager delegation
- GET /api/bookings returns company bookings for managers

---

### Test 2: Role-Based Access Control Enforcement

**Name:** Employees cannot book for others, managers can

**Components involved:**
- POST /api/auth/login (auth service)
- POST /api/bookings (booking service with middleware)
- JWT token structure

**Setup:**
- User with role=employee logged in (JWT token A)
- User with role=manager logged in (JWT token B)
- Provider with available slot seeded

**Steps:**
1. Call POST /api/auth/login with employee credentials → get JWT A (role=employee)
2. Call POST /api/bookings with provider_id, slot_id, booked_for_name, booked_for_email, JWT A
3. Call POST /api/auth/login with manager credentials → get JWT B (role=manager)
4. Call POST /api/bookings with provider_id, slot_id, booked_for_name, booked_for_email, JWT B

**Expected result:**
- Step 2: Returns 403 Forbidden with error "Insufficient permissions: only managers and department heads can book for others"
- Step 4: Returns 201 with booking_id, status='confirmed'

**Contract points validated:**
- JWT payload includes role field
- Middleware extracts role from JWT
- Role-based access control enforces permissions
- Error response format for 403

---

### Test 3: Department Head Scope Limitation

**Name:** Department heads can only book for employees in their department

**Components involved:**
- POST /api/auth/login (auth service)
- POST /api/bookings (booking service with middleware)
- Database (users table with department_id)
- JWT token structure

**Setup:**
- Department head with department_id=deptA logged in (JWT token)
- Employee in deptA seeded in database
- Employee in deptB seeded in database
- Provider with available slot seeded

**Steps:**
1. Call POST /api/auth/login with department head credentials → get JWT token
2. Call POST /api/bookings with provider_id, slot_id, booked_for_email=deptB_employee, JWT token
3. Call POST /api/bookings with provider_id, slot_id, booked_for_email=deptA_employee, JWT token

**Expected result:**
- Step 2: Returns 403 Forbidden with error "Department heads can only book for employees in their department"
- Step 3: Returns 201 with booking_id, status='confirmed'

**Contract points validated:**
- JWT payload includes department_id field
- Middleware queries booked_for user's department_id
- Department filtering logic enforced
- Cross-department access blocked

---

### Test 4: Datetime Format Consistency Across Services

**Name:** All services use ISO 8601 datetime format

**Components involved:**
- POST /api/bookings (booking service)
- GET /api/bookings (bookings retrieval service)
- GET /api/providers/:id (provider service)

**Setup:**
- Provider with time slots seeded in database

**Steps:**
1. Call GET /api/providers/:id
2. Extract start_time from first available_slot
3. Call POST /api/bookings with that slot_id
4. Call GET /api/bookings
5. Extract created_at from booking response

**Expected result:**
- Step 2: start_time is ISO 8601 string (e.g., "2025-03-15T14:30:00Z")
- Step 5: created_at is ISO 8601 string
- No Unix timestamps (numbers) in any response

**Contract points validated:**
- Contract 1: datetime format = ISO 8601
- Consistency across all API endpoints
- No date format mismatch between services

---

### Test 5: UUID Format Consistency Across Services

**Name:** All ID fields use UUID v4 format

**Components involved:**
- GET /api/providers (provider service)
- POST /api/bookings (booking service)
- GET /api/bookings (bookings retrieval service)

**Setup:**
- Provider and slots seeded in database

**Steps:**
1. Call GET /api/providers
2. Extract provider_id from response
3. Call GET /api/providers/:id to get slot_id
4. Call POST /api/bookings with provider_id, slot_id
5. Extract booking_id from response
6. Call GET /api/bookings

**Expected result:**
- Step 2: provider_id is UUID v4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
- Step 3: slot_id is UUID v4 string
- Step 5: booking_id is UUID v4 string
- Step 6: All IDs in response are UUID v4 format
- No integer IDs (e.g., 7, 123) in any response

**Contract points validated:**
- Contract 1: provider_id, service_id, slot_id, user_id, booking_id = UUID v4
- Consistency across all API endpoints
- No ID type mismatch between services
