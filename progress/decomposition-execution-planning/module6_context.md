# Module 6 Context: Parallel Execution

## Micro-Exercise: Parallel Tickets Analysis

**Tickets:**
- Ticket A: Build the provider availability API (providers set their open time slots)
- Ticket B: Build the booking creation API (users book a provider's time slot)
- Ticket C: Build the provider profile page (frontend displays provider info, ratings, services)
- Ticket D: Build the email notification service (sends booking confirmations)

### 1. Which 2 tickets can run simultaneously right now? Why?

**Tickets A and C can run simultaneously.**
- Ticket A is a backend API (provider availability)
- Ticket C is a frontend page (provider profile display)
- They work on different layers (backend vs frontend) with no blocking dependency
- They can work in parallel as long as they agree on the provider data shape contract

### 2. Which 2 tickets CANNOT run simultaneously? What is the dependency?

**Tickets A and B CANNOT run simultaneously.**
- Ticket B depends on Ticket A's output
- You cannot book a time slot if the availability API does not exist yet
- Booking creation needs to know which slots are available (from Ticket A) and needs to update slot status (through Ticket A's data model)
- This is a hard dependency - A must complete before B can start

### 3. For the 2 parallel tickets (A and C), what is the contract between them?

**Contract: Provider data shape agreement**

Both tickets must agree on the provider data structure:
- Provider ID format (UUID v4)
- Provider name (string, max 100 chars)
- Category (string, max 50 chars)
- Rating (decimal, 1-5 scale)
- Services array structure (service_id, name, description, price)
- Time slots array structure (slot_id, start_time, end_time, status)

Ticket A (backend API) must return this shape when queried. Ticket C (frontend) must consume this shape to display the profile. If Ticket A returns a different field name or data type, Ticket C's frontend will break at the sync point when they integrate.
