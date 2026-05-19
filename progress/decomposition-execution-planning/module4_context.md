# Module 4 Context: Vertical Slicing

## Micro-Exercise: Horizontal Layers vs Vertical Slice

**Requirement:** A user can book a service provider.

### Horizontal Layers
1. **Data Storage Layer** - Database schema for users, providers, services, time slots, bookings
2. **Backend Logic Layer** - API endpoints for fetching providers, checking availability, creating bookings, handling conflicts
3. **User Interface Layer** - Provider listing page, provider detail page, time slot selection, booking confirmation

### Minimal Vertical Slice
**Thinnest end-to-end booking:**

- **One hardcoded provider** (no provider search, just display one pre-configured provider)
- **One service** (single service type, no category browsing)
- **One time slot** (hardcoded slot at a specific date/time, no availability calendar UI)
- **One user** (hardcoded test user or simple login form)
- **Booking action:** User clicks "Book" button → system creates booking record → user sees "Booking confirmed" message
- **No payment** (mock payment or free booking)
- **No email notifications**
- **No cancellation**
- **No conflict detection** (assume slot is available)

This proves the concept: data stores, backend processes booking, UI displays result. Everything else (search, calendar, payments, emails) is a wider slice for later.
