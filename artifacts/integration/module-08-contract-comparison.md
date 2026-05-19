# Module 8: Contract Comparison

## Phase 1: Contract Comparison

### Contracts from Module 6

**Contract 1: Database Schema Shared Types**
- provider_id: uuid (v4)
- service_id: uuid (v4)
- slot_id: uuid (v4)
- user_id: uuid (v4)
- booking_id: uuid (v4)
- datetime format: ISO 8601 (e.g., "2025-03-15T14:30:00Z")
- rating: decimal (1-5 scale, 1 decimal place)
- price: decimal (2 decimal places)

**Contract 4: Seed DB <-> POST /api/bookings**
- Seed script creates slot_id values with status='available'
- POST /api/bookings must validate slot exists and status='available'
- POST /api/bookings must update time_slots.status to 'booked' in same transaction

**Contract 6: POST /api/auth/login <-> Future Tickets**
- JWT secret key from JWT_SECRET environment variable
- Token payload includes user_id (uuid v4)
- Token expiration: 24 hours
- Token format: Bearer <token> in Authorization header

### New Contracts from Module 7 (Role-Based Access)

**New: JWT Token Structure (from Module 7)**
- JWT payload now includes: user_id, email, role (enum: employee, manager, department_head), department_id (uuid), company_name
- Token expiration: 24 hours unchanged

**New: Role-Based Access Contract (from Module 7)**
- Employees can only book for themselves
- Managers can book for anyone in company
- Department heads can only book/view for employees in their department
- Middleware checks role from JWT on booking endpoints

### Contract Mismatches Found

**No mismatches found between Module 6 and Module 7 contracts.**

The Module 7 contracts extend the Module 6 contracts without breaking changes:
- JWT payload is extended with role/department_id (backward compatible)
- Role-based access is added as additional validation, not replacing existing logic
- Datetime format remains ISO 8601 (no change to Unix timestamps)
- UUID v4 format remains consistent

### Contract Completeness Check

**Missing contract: Notification Service Integration**
- No contract defined for how booking service notifies providers
- No specification of notification payload structure
- No specification of notification delivery mechanism (email, SMS, in-app)
- This is a gap that could cause integration issues if notification service is added

**Recommendation:** Define notification contract before integrating notification service to avoid date format mismatch like the micro-exercise example.
