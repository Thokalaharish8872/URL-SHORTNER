# Module 8 Break: Integration Bug Diagnosis

## Symptom
"The provider does not see new bookings on their dashboard."

## Debugging Process

**Step 1: Verify bookings are being created**
- Check the booking database or API response from POST /api/bookings
- Booking creation flow works - bookings are being created successfully
- API response shows: booking_id, status="confirmed", created_at, provider_id, slot_id
- Database query confirms: bookings exist with status="confirmed"

**Step 2: Verify the dashboard is fetching bookings**
- Check the dashboard's API call to the booking service or its own data store
- Dashboard loads and displays correctly - it's fetching booking data
- Dashboard API query: SELECT * FROM bookings WHERE provider_id = ? AND status = 'active'
- Dashboard is filtering for status="active"

**Step 3: Notice the mismatch**
- Created bookings have status="confirmed"
- Dashboard is filtering for status="active"
- The status values don't match
- This is a contract mismatch between the booking service and the dashboard

**Step 4: Root cause analysis**
- Booking service spec: When booking is successfully created, its status is "confirmed"
- Dashboard spec: Dashboard shows all "active" bookings for the provider
- Both components are working exactly as specified
- Both pass their individual acceptance criteria
- The bug exists in the space between them: no shared definition of what status values exist and which ones mean "this booking should be visible to the provider"
- Booking service uses "confirmed" to mean "this is a real, valid booking"
- Dashboard uses "active" to mean "this booking is current and should be shown"
- They are expressing the same concept with different words

## Diagnosis
This is a contract mismatch, not a bug in either component. The interface contract between the booking service and the provider dashboard did not define a shared status enum. Each component made its own assumption about status values, and those assumptions don't align.

## Fix Options
1. Update booking service to use status="active" instead of "confirmed"
2. Update dashboard to filter for status="confirmed" instead of "active"
3. Define a shared status enum contract with values like "confirmed", "cancelled", "completed" and have both components use the same values
4. Add a status mapping layer that translates "confirmed" to "active" for the dashboard

The correct fix is option 3: define a shared contract that both components agree on, then update both components to use the shared status enum.
