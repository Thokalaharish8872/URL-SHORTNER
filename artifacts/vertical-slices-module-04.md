# Module 4: Vertical Slices - SkillSwap

## Slice 1: Browse and Book (Seeded Data)

**Scope:** User visits the app and sees a list of 3 service providers with name, category, and rating. User clicks a provider and sees their profile with one service listed and 3 available time slots. User selects a time slot and clicks "Book." User sees a confirmation screen with booking ID, provider name, service name, and booked time. Booking is persisted to the database.

**Anti-scope:** No user authentication (anonymous usage). No payment processing (booking is free). No email or push notifications. No search or filtering. No provider registration or management interface. No cancellation or modification of bookings. No reviews or ratings submission. No real-time availability checking (time slots are static seed data). No multi-city support. No admin dashboard.

**Dependencies:** None (first slice).

**Acceptance criteria:**
1. Open the app — see 3 provider cards with name, category, star rating
2. Click any provider — see profile page with service description and 3 time slots
3. Select a time slot and click "Book Now"
4. See confirmation page with booking reference number, provider name, service, and time
5. Refresh the page — booking persists (it is stored, not just in-memory)

**Estimated complexity:** S (2-3 hours)

---

## Slice 1.5: Payment Spike (Standalone)

**Scope:** Standalone page demonstrating Stripe test-mode payment flow. User enters test card details and clicks "Pay." Stripe processes payment and returns success/failure. Platform displays transaction status. No integration with booking flow - this is a proof-of-concept to show money can flow through the platform.

**Anti-scope:** No integration with booking system. No user authentication. No commission calculation. No refund flow. No webhook handling. No payment history. No saved payment methods. No invoice generation. Single hardcoded amount ($50).

**Dependencies:** None (standalone proof-of-concept).

**Acceptance criteria:**
1. Open payment spike page - see payment form with amount $50
2. Enter valid Stripe test card details - click "Pay"
3. See "Payment Successful" with transaction ID
4. Enter invalid card details - see "Payment Failed" error
5. Stripe dashboard shows test transaction

**Estimated complexity:** S (2-3 hours)

---

## Slice 2: User Authentication

**Scope:** Users can register with email/password, log in, and log out. Logged-in users see their name in the header. Booking flow now associates bookings with the authenticated user. Users can view their own bookings on a "My Bookings" page.

**Anti-scope:** No social login (Google, Facebook). No password reset flow. No email verification. No profile editing. No two-factor authentication. No role-based access control (all users are customers). No OAuth integration.

**Dependencies:** Slice 1 (Browse and Book) - builds on booking data model.

**Acceptance criteria:**
1. Click "Sign Up" — enter email and password — see "Registration successful"
2. Click "Log In" — enter credentials — see "Welcome, [name]" in header
3. Click "Log Out" — see login page
4. Book a service while logged in — see booking on "My Bookings" page
5. Log out — "My Bookings" page is no longer accessible

**Estimated complexity:** M (1-2 days)

---

## Slice 3: Provider Self-Service

**Scope:** Providers can register, create their profile (name, description, category), add services with pricing, and set availability time slots. Provider profiles are visible in the provider list. Provider can view their own bookings and earnings summary.

**Anti-scope:** No provider vetting/approval workflow (auto-approved). No photo uploads for profiles. No service categories management (fixed list). No advanced availability patterns (repeating schedules, blocked dates). No provider analytics beyond basic earnings. No provider-to-provider messaging.

**Dependencies:** Slice 1 (Browse and Book) - builds on provider data model. Slice 2 (User Authentication) - providers use same auth system.

**Acceptance criteria:**
1. Click "Become a Provider" — register as provider
2. Create profile with name, description, category — see profile saved
3. Add service with price — see service listed on profile
4. Add time slots for availability — see slots listed
5. As a provider, see own bookings and earnings summary

**Estimated complexity:** M (1-2 days)

---

## Slice 4: Payment Processing

**Scope:** Users pay for bookings via Stripe integration. Booking flow now requires payment before confirmation. Booking status changes from "pending" to "confirmed" after successful payment. Platform calculates and stores 15% commission. Users receive on-screen payment confirmation.

**Anti-scope:** No refund processing. No partial payments. No payment plans. No invoice generation. No payout to providers (commission stored but not yet paid out). No multiple payment methods (credit card only). No saved payment methods. No payment history page.

**Dependencies:** Slice 1 (Browse and Book) - extends booking flow. Slice 2 (User Authentication) - payment associated with user.

**Acceptance criteria:**
1. Select time slot and click "Book" — see payment form with amount
2. Enter valid test card details — see "Payment Successful"
3. See booking confirmed with status "confirmed"
4. View booking details — see payment amount and commission calculated
5. Invalid card details — see payment error and booking not confirmed

**Estimated complexity:** M (2-3 days)

---

## Slice 5: Real-Time Availability and Conflict Detection

**Scope:** Time slots are dynamically managed based on actual availability. When a user books a slot, it becomes unavailable to others. Conflict detection prevents double-booking. Provider can edit availability in real-time.

**Anti-scope:** No waitlist for fully booked slots. No automated availability suggestions. No calendar sync with external calendars (Google, Outlook). No timezone support (single timezone). No buffer time between appointments. No recurring availability patterns.

**Dependencies:** Slice 1 (Browse and Book) - extends availability system. Slice 3 (Provider Self-Service) - providers manage their availability.

**Acceptance criteria:**
1. Provider adds time slot — see slot available for booking
2. User books slot — slot becomes unavailable for others
3. Two users try to book same slot simultaneously — only one succeeds
4. Provider edits availability — changes reflected immediately
5. Provider removes slot — existing bookings for that slot remain

**Estimated complexity:** L (3-4 days)
