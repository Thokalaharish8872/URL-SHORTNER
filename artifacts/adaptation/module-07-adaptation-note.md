# Module 7: Impact Statement for PM (Updated with Role-Based Access)

## To: Product Manager
## Subject: Meridian Demo Plan - 6-Day Timeline (Updated with Role-Based Access)

With the Meridian company accounts requirement, the new role-based access requirement (managers, employees, department heads), and the compressed 6-day timeline, here is where we land:

**What you are getting in 6 days:**
- Individual booking flow (users book for themselves) - fully functional
- Role-based company-account booking with three roles (employee, manager, department head) - fully functional with role-based permissions
- Department visibility: department heads can only see/book for their department, managers see entire company
- Provider listing with 3 seeded providers - functional
- User authentication with company name, role, and department support - functional
- Booking confirmation with delegation info - functional
- My Bookings page with role-based filtering (employees see own bookings, managers see company bookings, department heads see department bookings) - functional

**What you are NOT getting in 6 days (and when to expect it):**
- Payment processing - CUT from demo scope. Will use simulated payment confirmation. Shipping week after demo.
- Provider self-service (providers register and manage their own profiles) - shipping week after demo
- Real-time availability and conflict detection - shipping week after demo (static seeded slots sufficient for demo)
- Provider dashboard - shipping week after demo
- Advanced search/filtering - shipping week after demo
- Email notifications - shipping week after demo (on-screen confirmation sufficient for demo)

**What is at risk:**
- Timeline is very tight: 29-38 hours of work over 6 days = 5-6 hours/day required
- Role-based access complexity may exceed estimates - if any single ticket takes 2x estimate, the demo is at risk
- Payment processing is cut - we will demo with simulated payment confirmation, not live Stripe. This is a deliberate cut to make room for role-based access.

**What I need from you:**
- An introduction to the Meridian IT contact so I can confirm the exact role definitions and department structure they need
- Confirmation that the three-role model (employee, manager, department_head) is sufficient, or if they need more granular roles
- Confirmation that simulated payment confirmation is acceptable for the demo, or if live payments are a hard requirement (which would require cutting something else to make room)
- Access to Meridian's branding assets (logo, colors) if you want the demo to look customized for them

**Scope change impact:**
The role-based access requirement significantly increased complexity. We went from a simple "can_book_for_others flag" to a full role/department model with permission checks on every endpoint. To accommodate this, we had to cut payment processing from the demo scope. The tradeoff is: we will show sophisticated role-based booking, but without real payments. If live payments are a hard requirement, we need to cut something else (likely the department-level visibility - simplify to just manager/employee roles without departments).

**Tradeoff summary:**
We are cutting provider-facing features, advanced search, and payment processing to focus entirely on the role-based booking experience that Meridian needs. The demo will nail the core use case (role-based booking with department visibility) but will not show the full product vision. The cut features are scheduled for the week after demo, funded by the Meridian deal if it closes.

Let me know immediately if payment processing is a hard requirement for the demo - I need to know whether to proceed with the current plan or make additional cuts.
