# Module 7: Updated Plan for 6-Day Demo (With Role-Based Access)

## 1. Preserved Tickets (Unchanged)

- **Ticket 2: GET /api/providers - List Providers** - DONE, no changes
- **Ticket 3: GET /api/providers/:id - Get Provider Details** - DONE, no changes

## 2. Modified Tickets (Changes Required - Escalated Impact)

- **Ticket 1: Seed Database with Test Provider Data** - DONE, needs modification
  - Changes: Add roles table seed data (employee, manager, department_head). Add departments table seed data. Update user seed data to include role and department_id assignments.
  - Estimate: S (1-2 hours) - escalated from NO IMPACT

- **Ticket 4: POST /api/bookings - Create a Booking** - DONE, needs modification
  - Changes: Add optional `booked_for_name` and `booked_for_email` fields. Add role-based access check: only managers and department heads can book for others. Employees can only book for themselves. Add department filtering: department heads can only view/book for employees in their department. Update response to include delegation info.
  - Estimate: L (4-5 hours) - escalated from M (3-4 hours)

- **Ticket 5: POST /api/auth/register - User Registration** - DONE, needs modification
  - Changes: Add `company_name`, `role` (enum: employee, manager, department_head), and `department_id` fields to request body. Update JWT token generation to include role and department_id in payload. Update response to include role and department.
  - Estimate: M (2-3 hours) - escalated from S (1 hour)

- **Ticket 6: POST /api/auth/login - User Login** - DONE, needs modification
  - Changes: Update JWT token generation to include role and department_id from user record. Update response to include role and department.
  - Estimate: M (1-2 hours) - escalated from NO IMPACT

## 3. Cut Tickets (Removed from 6-Day Scope)

- **Provider Self-Service (Slice 3)** - CUT
  - Why: Not required for Meridian demo. Meridian is booking services, not providing them.

- **Real-Time Availability and Conflict Detection (Slice 5)** - CUT
  - Why: Static seeded slots sufficient for demo with role-based access.

- **Provider Dashboard** - CUT
  - Why: Not required for Meridian demo.

- **Search/Filtering** - CUT
  - Why: Basic listing with 3 seeded providers sufficient.

- **Email Notifications** - CUT
  - Why: On-screen confirmation sufficient.

- **Payment Processing (Slice 4)** - CUT (escalated from SHOULD SHIP)
  - Why: Must cut to make room for role-based access complexity. Will use simulated payment confirmation.

## 4. Added Tickets (New for Company Accounts + Role-Based Access)

- **Ticket 7: Database Migration - Add Role-Based Access Tables**
  - Scope: Create roles table (id, name, permissions). Create departments table (id, name, company_name). Add role and department_id columns to users table. Create migration script.
  - Estimate: M (2-3 hours)

- **Ticket 8: POST /api/auth/register - Add Role and Department Fields**
  - Scope: Update registration to accept company_name, role (dropdown), department_id (dropdown). Validate role exists, department exists for company. Update JWT payload.
  - Estimate: M (2-3 hours)

- **Ticket 9: POST /api/auth/login - Update JWT with Role/Department**
  - Scope: Update login to fetch user's role and department_id, include in JWT token payload. Return role and department in response.
  - Estimate: S (1-2 hours)

- **Ticket 10: POST /api/bookings - Add Delegation + Role-Based Access**
  - Scope: Add booked_for_name/email fields. Add middleware to check user role from JWT. Enforce: employees can only book for themselves, managers can book for anyone in company, department heads can only book/view for their department. Update database transaction.
  - Estimate: L (4-5 hours)

- **Ticket 11: Frontend - Registration Form with Role/Department**
  - Scope: Add company_name input, role dropdown (employee/manager/department_head), department dropdown (filtered by company_name). Role selection determines available departments.
  - Estimate: M (2-3 hours)

- **Ticket 12: Frontend - Booking Form with Role-Based Delegation**
  - Scope: Add conditional "Who is this booking for?" section when user role is manager or department_head. Hide for employees. For department heads, filter employee list to show only employees in their department. Add validation.
  - Estimate: L (4-5 hours)

- **Ticket 13: Frontend - Booking Confirmation with Delegation**
  - Scope: Show "Booked for: [name]" when delegation occurred. Show regular confirmation for non-delegated.
  - Estimate: S (1 hour)

- **Ticket 14: GET /api/bookings - Role-Based Bookings Endpoint**
  - Scope: Create endpoint with role-based filtering: employees see own bookings, managers see all company bookings, department heads see department bookings. Return bookings with delegation info.
  - Estimate: M (2-3 hours)

- **Ticket 15: Frontend - My Bookings Page with Role Filtering**
  - Scope: Create page to display bookings with role-based filtering. Show different views based on user role (own bookings vs company bookings vs department bookings).
  - Estimate: M (3-4 hours)

## Timeline Summary

**Preserved work:** 2 tickets (DONE) = 0 hours
**Modified work:** 4 tickets = 8-12 hours (escalated from 4-5 hours)
**New work:** 9 tickets = 21-26 hours (escalated from 13-15 hours)
**Total additional work:** 29-38 hours over 6 days = ~5-6 hours/day

**Risk items:**
- Timeline is now very tight (5-6 hours/day required)
- Payment processing cut - will use simulated payment confirmation
- Role-based access complexity may exceed estimates
- If any single ticket takes 2x estimate, the demo is at risk

## Decision Re-evaluation

Option B (Minimal Bridge) is becoming expensive. With roles, departments, and permission logic, the "minimal bridge" is now:
- 2 new database tables (roles, departments)
- Role-based access middleware on all booking endpoints
- JWT payload changes
- Complex frontend role/department selection

This is approaching Option A complexity, but with 6 days to demo, pivoting to Option A (proper redesign) would miss the deadline. Staying with Option B but acknowledging significantly increased risk.
