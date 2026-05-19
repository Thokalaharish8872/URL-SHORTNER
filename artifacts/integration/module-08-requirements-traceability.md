# Module 8: Requirements Traceability Matrix

## Phase 4: Requirements Traceability Check

### From Module 1 Requirements (requirements/module-01-full-extraction.md)

| Requirement | Status | Location | Notes |
|-------------|--------|----------|-------|
| Users can browse providers | Built | GET /api/providers (Ticket 2) | Returns provider list with name, category, rating |
| Users can view provider details including services and availability | Built | GET /api/providers/:id (Ticket 3) | Returns provider details, services array, available_slots |
| Users can book time slots | Built | POST /api/bookings (Ticket 4) | Creates booking, updates slot status to 'booked' |
| Booking confirmation includes booking details | Built | POST /api/bookings response | Returns booking_id, provider_id, slot_id, status, created_at |
| Users can register accounts | Built | POST /api/auth/register (Ticket 5) | Creates user with email, password_hash |
| Users can login | Built | POST /api/auth/login (Ticket 6) | Returns JWT token with user_id |
| Company accounts support | Built | Users table (company_name column), Ticket 8 | Users can register with company_name |
| Role-based access (manager, employee, department head) | Built | Roles table, Ticket 10 middleware | JWT includes role, middleware enforces permissions |
| Department-level visibility | Built | Departments table, Ticket 14 endpoint | Department heads see department bookings |
| Managers can book for employees | Built | Ticket 10 POST /api/bookings | Delegation fields, role validation |
| Cancellation policy (24 hours advance notice, full refund) | Deferred | Not in 6-day scope | Deferred to week after demo |
| Provider can set their own availability | Deferred | Provider Self-Service (Slice 3) CUT | Deferred to week after demo |
| Provider can view their bookings | Deferred | Provider Dashboard CUT | Deferred to week after demo |
| Provider can manage their profile | Deferred | Provider Self-Service CUT | Deferred to week after demo |
| Search/filter providers by category | Deferred | Search/Filtering CUT | Deferred to week after demo |
| Email notifications for bookings | Deferred | Email Notifications CUT | Deferred to week after demo |
| Real-time availability with conflict detection | Deferred | Real-Time Availability CUT | Deferred to week after demo |
| Payment processing with Stripe | Deferred | Payment Processing CUT | Will use simulated payment for demo |

### Requirements Status Summary

**Built (6 core requirements):**
- Browse providers, view details, book slots, booking confirmation, registration, login
- Company accounts, role-based access, department visibility, manager delegation

**Deferred (8 requirements):**
- Cancellation policy, provider self-service, provider dashboard, search, email notifications, real-time availability, payment processing
- All deferred to week after demo or handled via simulation (payment)

**Lost (0 requirements):**
- No requirements lost - all Module 1 requirements are either built or explicitly deferred

### Simplified Requirements

**Payment Processing:**
- Original: Full Stripe integration with live payments
- Simplified: Simulated payment confirmation for demo
- Reason: Timeline compression - cut from SHOULD SHIP to CUT to make room for role-based access complexity

**Cancellation Policy:**
- Original: 24-hour advance notice, full refund, partial refund for less notice
- Simplified: Not implemented in 6-day scope
- Reason: Not required for Meridian demo focus on role-based booking

### Traceability Notes

**Good practices observed:**
- Every requirement from Module 1 has a status
- Deferred requirements have explicit reasons and timeline (week after demo)
- No requirements were "lost" - all accounted for
- Built requirements map to specific tickets and components

**Potential gaps:**
- Notification service integration not defined (not in Module 1 requirements, but may be needed for production)
- Admin/management interface for Meridian not specified (may need to be added post-demo)
