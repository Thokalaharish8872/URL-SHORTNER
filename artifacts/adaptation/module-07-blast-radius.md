# Module 7: Blast Radius Analysis

## Change 1: Company Accounts (Minimal Bridge Approach)

### Database Schema

| Artifact | Status | Impact |
|----------|--------|--------|
| Users table | Schema exists | MAJOR: Add company_name (varchar(255), nullable), role (enum: employee, manager, department_head), department_id (uuid, nullable), can_book_for_others (boolean, derived from role). Need new roles table, departments table, and foreign keys. 2-3 hours for migration. |
| Roles table | New | MAJOR: Create roles table with role definitions (employee, manager, department_head). Define permissions per role. 1 hour. |
| Departments table | New | MAJOR: Create departments table with department_id, department_name, company_name. Link users to departments. 1 hour. |
| Bookings table | Schema exists | MINOR: Add booked_for_name and booked_for_email columns to bookings table. 30 minutes for migration. |
| Providers table | Schema exists | NO IMPACT: Company accounts don't affect provider data. |
| Services table | Schema exists | NO IMPACT: Company accounts don't affect services. |
| Time slots table | Schema exists | NO IMPACT: Company accounts don't affect slots. |

### API Endpoints

| Artifact | Status | Impact |
|----------|--------|--------|
| POST /api/auth/register | Ticket 5 DONE | MAJOR: Add company_name, role (enum), department_id fields to request body. Update JWT token to include role and department_id. Update response to include role and department. 2-3 hours. |
| POST /api/auth/login | Ticket 6 DONE | MAJOR: Update JWT token generation to include role and department_id from user record. Update response to include role and department. 1-2 hours. |
| GET /api/providers | Ticket 2 DONE | NO IMPACT: Listing providers doesn't change with role-based access. |
| GET /api/providers/:id | Ticket 3 DONE | NO IMPACT: Provider details don't change with role-based access. |
| POST /api/bookings | Ticket 4 DONE | MAJOR: Add optional booked_for_name and booked_for_email to request body. Add role-based access check: only managers and department heads can book for others. Employees can only book for themselves. Add department visibility: department heads can only view bookings in their department. Update response to include delegation info. Update database transaction. 4-5 hours. |
| GET /api/bookings | New ticket | MAJOR: Create endpoint to retrieve bookings with role-based filtering: employees see own bookings, managers see all company bookings, department heads see department bookings. 2-3 hours. |

### Frontend Components

| Artifact | Status | Impact |
|----------|--------|--------|
| Registration form | Not started | MAJOR: Add company_name, role (dropdown), department_id (dropdown) fields. Role determines available options. 2-3 hours. |
| Login form | Not started | NO IMPACT: Login unchanged. |
| Provider listing page | Not started | NO IMPACT: Listing doesn't show company info. |
| Provider detail page | Not started | NO IMPACT: Detail page doesn't show company info. |
| Booking form | Not started | MAJOR: Add conditional "Who is this booking for?" section (name, email) when user role is manager or department_head. Hide for employees. Add validation. Add department filtering for department heads (can only book for employees in their department). 4-5 hours. |
| Booking confirmation page | Not started | MINOR: Show "Booked for: [name]" when delegation occurred. 1 hour. |
| My Bookings page | Not started | MAJOR: Role-based filtering: employees see own bookings, managers see all company bookings, department heads see department bookings. 3-4 hours. |

### Interface Contracts

| Artifact | Status | Impact |
|----------|--------|--------|
| Contract 1: Database Schema | Created | MAJOR: Update to include roles table, departments table, user role/department_id columns, role-based permissions. |
| Contract 2: Seed DB <-> GET /api/providers | Created | NO IMPACT: Provider listing unchanged. |
| Contract 3: GET /api/providers <-> GET /api/providers/:id | Created | NO IMPACT: Provider endpoints unchanged. |
| Contract 4: Seed DB <-> POST /api/bookings | Created | MAJOR: Update POST /api/bookings contract to include optional booked_for_name and booked_for_email fields, role-based access constraints, department visibility rules. |
| Contract 5: POST /api/bookings <-> Future Tickets | Created | MAJOR: Future tickets (My Bookings) must handle booked_for fields and role-based filtering. |
| Contract 6: JWT Token Structure | New | MAJOR: Define JWT payload structure to include role and department_id. All authenticated endpoints must validate role permissions. |

### Tickets

| Artifact | Status | Impact |
|----------|--------|--------|
| Ticket 1: Seed Database | DONE | MAJOR: Need to seed roles data, departments data, update user seed data with role/department assignments. |
| Ticket 2: GET /api/providers | DONE | NO IMPACT: Provider listing unchanged. |
| Ticket 3: GET /api/providers/:id | DONE | NO IMPACT: Provider details unchanged. |
| Ticket 4: POST /api/bookings | DONE | MAJOR: Need to modify to support delegation fields, role-based access checks, department filtering. |
| Ticket 5: POST /api/auth/register | DONE | MAJOR: Need to add company_name, role, department_id fields, update JWT generation. |
| Ticket 6: POST /api/auth/login | DONE | MAJOR: Need to update JWT generation to include role and department_id. |

## Change 3: Role-Based Access Control (New Requirement)

### Database Schema (Additional Impact)

| Artifact | Status | Impact |
|----------|--------|--------|
| Roles table | New | MAJOR: Create roles table with role definitions (employee, manager, department_head) and permission mappings. 1 hour. |
| Departments table | New | MAJOR: Create departments table with department_id, department_name, company_name. Link users to departments via department_id foreign key. 1 hour. |
| User-role mapping table | New | MINOR: Join table if many-to-many roles needed, or use role column on users table for one-to-one. For demo: role column on users table is sufficient. |

### API Endpoints (Additional Impact)

| Artifact | Status | Impact |
|----------|--------|--------|
| POST /api/auth/register | Ticket 5 DONE | ESCALATED to MAJOR: Was MINOR for company_name only. Now needs role selection and department_id. |
| POST /api/auth/login | Ticket 6 DONE | ESCALATED to MAJOR: Was NO IMPACT. Now needs JWT payload update to include role and department_id. |
| POST /api/bookings | Ticket 4 DONE | ESCALATED to MAJOR: Was already MAJOR for delegation. Now adds role-based access checks and department filtering logic. |
| GET /api/bookings | New ticket | MAJOR: Role-based filtering endpoint required. |

### Frontend Components (Additional Impact)

| Artifact | Status | Impact |
|----------|--------|--------|
| Registration form | Not started | ESCALATED to MAJOR: Was MINOR for company_name. Now needs role dropdown and department dropdown. |
| Booking form | Not started | ESCALATED to MAJOR: Was already MAJOR. Now adds department filtering for department heads. |
| My Bookings page | Not started | MAJOR: Role-based filtering UI required. |

### What Changed from Original Assessment

**Artifacts that were NO IMPACT that are now MAJOR:**
- POST /api/auth/login: JWT token now carries role and department_id
- Ticket 1 (Seed Database): Now needs roles and departments seeded

**Artifacts that were MINOR that escalated to MAJOR:**
- POST /api/auth/register: Now needs role and department fields
- Registration form: Now needs role and department dropdowns

**New artifacts added:**
- Roles table
- Departments table
- GET /api/bookings endpoint
- JWT Token Structure contract

**Decision Re-evaluation:**
Option B (Minimal Bridge) is becoming expensive. The hack is growing into multiple tables, role-based access logic, and permission checks. The line between "minimal bridge" and "proper modeling" is blurring. However, with 6 days to demo, I cannot pivot to Option A (proper redesign) without missing the deadline. I will stay with Option B but acknowledge the increased complexity and risk.

## Change 2: Compressed Timeline (6 Days)

### Not-Started Tickets Categorization

| Ticket | Category | Rationale |
|--------|----------|-----------|
| Provider Self-Service (Slice 3) | CUT | Not required for Meridian demo. Meridian is booking services, not providing them. Can ship week after demo. |
| Payment Processing (Slice 4) | SHOULD SHIP | Demo is better with real payments, but can use simulated payment confirmation if Stripe setup takes too long. |
| Real-Time Availability (Slice 5) | CUT | Static seeded slots from Slice 1 are sufficient for demo. Real-time conflict detection not required for demo. |
| Provider Dashboard | CUT | Not required for Meridian demo. Meridian books services, doesn't need provider management UI. |
| Search/Filtering | CUT | Basic listing with 3 seeded providers is sufficient for demo. Advanced search not required. |
| My Bookings Page | MUST SHIP | Meridian needs to see bookings made by/for their employees. Critical for demo. |
| Email Notifications | CUT | On-screen confirmation is sufficient for demo. Email not required. |

### Completed/In-Progress Tickets

| Ticket | Category | Rationale |
|--------|----------|-----------|
| Ticket 1: Seed Database | PRESERVED | Done and unchanged. |
| Ticket 2: GET /api/providers | PRESERVED | Done and unchanged. |
| Ticket 3: GET /api/providers/:id | PRESERVED | Done and unchanged. |
| Ticket 4: POST /api/bookings | MODIFIED | Done, but needs modification for delegation fields. |
| Ticket 5: POST /api/auth/register | MODIFIED | Done, but needs modification for company_name field. |
| Ticket 6: POST /api/auth/login | PRESERVED | Done and unchanged. |
