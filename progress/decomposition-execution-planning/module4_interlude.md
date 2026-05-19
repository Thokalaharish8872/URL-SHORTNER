# Module 4 Interlude: Spotify Squad Model Reflection

## Question 1: What did vertical slicing cost Spotify, and how did they fix it?

**Cost:** Vertical slicing gave Spotify speed but created integration chaos. When Payment Squad changed billing data schema without notifying others, Subscription Squad's analytics broke. When Playlist Squad changed API pagination format, Social Squad's activity feed broke. Autonomy without explicit contracts produced speed followed by chaos.

**Fix:** Spotify didn't abandon squads (which would lose speed). They layered alignment structures on top:
- **Chapters:** Horizontal groups across squads to establish shared standards (API versioning, pagination contracts, schema change communication)
- **Tribes:** Clusters of related squads with shared leadership to see big picture and flag cross-squad impacts
- **Explicit interface contracts:** Documented APIs with public API rigor, versioned database schemas, backward-compatible event schemas

**Relationship between autonomy and contracts:** Speed comes from autonomy within a slice. Stability comes from contracts at the boundaries. Autonomy without contracts is chaos. Contracts without autonomy is bureaucracy. You need both - autonomy inside the slice, contracts at the seams.

## Question 2: Where are the boundaries in my SkillSwap decomposition?

**Boundaries between slices:**
- Slice 1 (browse/book) and Slice 2 (auth) both touch bookings data - if bookings schema changes, auth's "My Bookings" page breaks
- Slice 1 and Slice 3 (provider self-service) both touch providers data - provider profile schema changes could break provider listing
- Slice 2 and Slice 4 (payment processing) both touch bookings - payment integration depends on booking data format
- All slices touch the shared database - schema changes in one slice affect all others

**What would happen without contracts:**
If two teams owned Slice 1 and Slice 2 with no shared contract for booking data format, and Slice 1 changed the booking schema (e.g., renamed fields), Slice 2's "My Bookings" page would break silently. The team owning Slice 2 wouldn't know the schema changed because they don't own the database.

**Seams and what crosses them:**
- **Database seams:** Bookings table, providers table, users table - all slices read/write these
- **API seams:** Booking API, provider API - multiple slices call these
- **Event seams:** Booking created, payment processed - downstream slices consume these

**Have I defined what crosses them?**
No - my slice definitions don't explicitly document data formats, API contracts, or event schemas. I have dependencies listed but not the interface contracts between slices. This is a gap - I should add interface contract documentation to prevent the integration chaos Spotify experienced.
