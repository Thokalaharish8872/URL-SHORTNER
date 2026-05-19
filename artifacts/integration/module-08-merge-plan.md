# Module 8: Merge Workstreams Plan

## Phase 2: Merge Workstreams (Incremental Integration)

### Merge Order

**Stream 1: Auth/Database Layer (First)**
- Components: Users table, Roles table, Departments table, POST /api/auth/register, POST /api/auth/login, JWT generation
- Rationale: Touches the most contracts (JWT structure, user data model). Validates the foundation before adding booking logic.
- Contract touchpoints: JWT Token Structure, Database Schema

**Stream 2: Provider/Listing Layer (Second)**
- Components: Providers table, Services table, Time Slots table, GET /api/providers, GET /api/providers/:id
- Rationale: Independent of auth and booking. Validates provider data model and listing APIs.
- Contract touchpoints: Database Schema, Seed DB <-> GET /api/providers

**Stream 3: Booking/Delegation Layer (Third)**
- Components: Bookings table, POST /api/bookings, role-based middleware, GET /api/bookings
- Rationale: Depends on auth (for role checks) and providers (for slot validation). Most complex integration point.
- Contract touchpoints: Seed DB <-> POST /api/bookings, POST /api/auth/login <-> Authenticated Endpoints

### Merge Process for Each Stream

**Stream 1: Auth/Database Layer**

1. **Merge code:** Combine database migrations for roles, departments, user role/department columns. Merge auth endpoints with JWT role/department payload.

2. **Run acceptance criteria:**
   - POST /api/auth/register: Can user register with company_name, role, department_id? Does JWT include role/department?
   - POST /api/auth/login: Does login return role/department? Does JWT include role/department?
   - Database: Are roles table and departments table created? Do user records have role/department_id?

3. **Run cross-component smoke test:**
   - Register user with role=manager, department_id=dept1
   - Login as that user
   - Decode JWT token
   - Verify role=manager and department_id=dept1 are present

4. **Document result:**
   - Merged: Auth/Database layer
   - Passed: Registration with role/department, login with JWT payload
   - Broke: None
   - Fixed: None

**Stream 2: Provider/Listing Layer**

1. **Merge code:** Combine provider, service, time slot tables and listing endpoints.

2. **Run acceptance criteria:**
   - GET /api/providers: Returns list of providers with correct data shapes
   - GET /api/providers/:id: Returns provider details with services and available slots
   - Database: Provider/service/slot data seeded correctly

3. **Run cross-component smoke test:**
   - Call GET /api/providers
   - Select first provider_id from response
   - Call GET /api/providers/:id with that ID
   - Verify response includes services and available_slots
   - Verify slot_id format is UUID v4
   - Verify slot times are ISO 8601 format

4. **Document result:**
   - Merged: Provider/Listing layer
   - Passed: Provider listing, provider details, data formats
   - Broke: None
   - Fixed: None

**Stream 3: Booking/Delegation Layer**

1. **Merge code:** Combine bookings table, POST /api/bookings with role-based middleware, GET /api/bookings endpoint.

2. **Run acceptance criteria:**
   - POST /api/bookings (employee): Employee books for themselves - succeeds
   - POST /api/bookings (employee): Employee tries to book for others - fails with 403
   - POST /api/bookings (manager): Manager books for others - succeeds
   - POST /api/bookings (department head): Department head books for department - succeeds
   - POST /api/bookings (department head): Department head tries to book for other department - fails with 403
   - GET /api/bookings: Employee sees own bookings
   - GET /api/bookings: Manager sees all company bookings
   - GET /api/bookings: Department head sees department bookings
   - Database: Slot status updates to 'booked' on successful booking

3. **Run cross-component smoke test:**
   - Login as manager (JWT with role=manager)
   - Call GET /api/providers to get provider_id
   - Call GET /api/providers/:id to get slot_id
   - Call POST /api/bookings with provider_id, slot_id, booked_for_name, booked_for_email
   - Verify booking created with status='confirmed'
   - Verify slot status updated to 'booked'
   - Call GET /api/bookings
   - Verify booking appears in response with delegation info

4. **Document result:**
   - Merged: Booking/Delegation layer
   - Passed: Employee restrictions, manager delegation, department filtering, slot status update
   - Broke: None
   - Fixed: None
