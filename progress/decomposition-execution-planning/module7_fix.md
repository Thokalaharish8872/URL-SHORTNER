# Module 7 Fix: Plan Layering and Role-Based Access Approach

## Structural Layering: Built on Adaptation vs Reverted to Scratch

**I built on my adaptation.** The second plan is not a rewrite from scratch - it's an evolution of the first plan:

- Preserved the blast radius table structure and expanded it with a new section "Change 3: Role-Based Access Control"
- Preserved the original categorization (PRESERVED, MODIFIED, CUT, ADDED) and updated the entries within each category
- Preserved the impact statement structure and revised the content to acknowledge the contradiction
- Did not throw away the original thinking about what to cut (provider self-service, real-time availability, etc.) - those cuts remain valid
- Added new escalations (e.g., Ticket 5 from MINOR to MAJOR, Ticket 6 from NO IMPACT to MAJOR) rather than re-evaluating everything

**Evidence:** The blast radius document shows three distinct changes (Company Accounts, Timeline Compression, Role-Based Access) layered on top of each other, not a single merged view.

## Role-Based Access Implementation: Minimal Bridge vs Proper Model

**The role-based access requirement tipped the scale from Option B toward Option A complexity, but I stayed with Option B.**

**Original Option B (Minimal Bridge):**
- company_name field on users table
- can_book_for_others boolean flag
- booked_for_name/email columns on bookings table

**Current approach after role requirement:**
- roles table (employee, manager, department_head)
- departments table (department_id, department_name, company_name)
- role column on users table (enum)
- department_id column on users table (foreign key)
- JWT token includes role and department_id
- Middleware checks role on booking endpoints
- can_book_for_others is now derived from role (manager/department_head = true, employee = false)

**Why this is still Option B:**
- No Organization entity (no proper org model)
- No many-to-many user-role relationships (one role per user)
- No permission system beyond hardcoded role checks
- No approval workflows
- Departments are simple flat structure, not hierarchical

**Why it's approaching Option A:**
- Multiple tables (roles, departments) instead of just columns
- Role-based access middleware on endpoints
- JWT payload changes
- Complex permission logic (department heads limited to their department)

**Decision:** Staying with Option B because with 6 days to demo, pivoting to Option A (proper Organization entity, full permission system) would miss the deadline. The current approach is a "maximal bridge" - pushing Option B to its limit but still not a proper model.

## Impact Statement Change and Acknowledgment

**The impact statement changed and explicitly acknowledges the contradiction:**

Original statement said: "Payment processing - SHOULD SHIP but may use simulated confirmation if Stripe setup takes too long."

Revised statement says: "Payment processing - CUT from demo scope. Will use simulated payment confirmation."

**Acknowledgment in revised statement:**
"The role-based access requirement significantly increased complexity. We went from a simple 'can_book_for_others flag' to a full role/department model with permission checks on every endpoint. To accommodate this, we had to cut payment processing from the demo scope."

This maintains credibility by explicitly stating: "In my earlier message I said we could hit payment processing in 6 days. With the role-based access requirement, payment processing is now cut to make room. Here is the revised scope."

## Role-Based Access Approach (Walkthrough)

**Where do roles live in the data model?**
- roles table: id (uuid), name (enum: employee, manager, department_head), permissions (json or hardcoded)
- users table: role (enum, foreign key to roles), department_id (uuid, foreign key to departments)
- departments table: id (uuid), department_name (varchar), company_name (varchar)

**How does a booking endpoint know whether the current user is a manager or an employee?**
- JWT token payload includes: { user_id, email, role, department_id, company_name }
- Middleware on POST /api/bookings extracts role from JWT
- Middleware checks: if role === 'employee', reject request if booked_for_name/email fields are present
- If role === 'manager' or 'department_head', allow delegation fields
- If role === 'department_head', additional check: verify booked_for user's department_id matches current user's department_id

**What happens when someone with "employee" role tries to hit the "book for someone else" endpoint?**
- Request arrives with booked_for_name and booked_for_email fields
- Middleware extracts role from JWT token (role = 'employee')
- Middleware checks: employee.role !== 'manager' && employee.role !== 'department_head'
- Middleware returns 403 Forbidden with error: "Insufficient permissions: only managers and department heads can book for others"
- Booking is not created

**What happens when a department head tries to book for someone outside their department?**
- Request arrives with booked_for_email for user in different department
- Middleware extracts role (role = 'department_head') and department_id from JWT
- Middleware queries users table to find booked_for user's department_id
- Middleware checks: current_user.department_id !== booked_for_user.department_id
- Middleware returns 403 Forbidden with error: "Department heads can only book for employees in their department"
- Booking is not created

## Plan Version Count

**The plan changed 3 times in this module:**
1. **Original plan from Module 6:** 6 tickets for Slice 1 and Slice 2, vertical slicing strategy
2. **First adaptation (Company Accounts + Timeline Compression):** Added 8 new tickets, modified 2 tickets, cut 5 tickets, 17-20 hours over 6 days
3. **Second adaptation (Role-Based Access):** Escalated 4 tickets from NO IMPACT/MINOR to MAJOR, added 1 new ticket (JWT contract), cut 1 additional ticket (Payment Processing), 29-38 hours over 6 days

**This demonstrates the plan is a living document that reflects current knowledge, not what was known yesterday.**
