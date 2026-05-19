# Module 4 Verification

## Clickthrough Test for Slice 1

**Can I test Slice 1 without reading any code?**

Yes. User experience walkthrough:
1. Open browser and navigate to app URL
2. See 3 provider cards displayed with name, category, star rating
3. Click on "Maria's Cleaning" provider card
4. See profile page with service description and 3 time slots (10am, 2pm, 5pm)
5. Select the 2pm time slot
6. Click "Book Now" button
7. See confirmation page showing booking reference number "BK-12345", provider name "Maria's Cleaning", service "House Cleaning", and time "2:00 PM"

No technical knowledge required - purely UI-driven verification.

## What I Learn From This Slice

**ONE thing learned:** Whether the booking flow UX makes sense to users. Specifically: Is picking from a list of 3 providers and selecting a time slot intuitive? Does the confirmation page provide enough information? This validates the core product hypothesis before investing in authentication, payments, or provider self-service.

## Red Flags Check

**Too thick?** No - Slice 1 is S complexity (2-3 hours), includes only browse and book with seeded data. No auth, payment, or notifications.

**Too thin?** No - has actual behavior (user browses, selects, books, sees confirmation). Not just a health endpoint or static page.

**Vague anti-scope?** No - specific list of 10+ items explicitly excluded (no auth, no payment, no email, no search, etc.). Stakeholder can point to anti-scope to answer "where is search?"

**No human-testable acceptance criteria?** No - all 5 criteria are UI-based (see providers, click provider, select slot, see confirmation, refresh persists). No "check database" or "API returns JSON" steps.

**Slices build on each other?** Yes - Slice 2 depends on Slice 1 (booking data model), Slice 3 depends on Slice 1 and 2 (provider data model, auth), Slice 4 depends on Slice 1 and 2 (booking flow, auth), Slice 5 depends on Slice 1 and 3 (availability, provider self-service).
