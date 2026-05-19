# Module 3: Revised Risk-Based Build Plan - Business Blocker Handling

## Business Blocker

**Issue:** Client has no Stripe account, business entity, or merchant account. Payment processing is blocked by business/legal infrastructure, not technical issues.

## Updated Build Order

1. **User Authentication** (Risk: 2, Dependency)
   - Justification: Required by almost everything. Low risk but unblocks the most work.

2. **Listings Data Model** (Risk: 2, Dependency)
   - Justification: Foundation for booking and search. Build early to unblock dependent work.

3. **Availability Management** (Risk: 4, Novelty)
   - Justification: High novelty risk (concurrency). Build early to surface race condition problems.

4. **Payment Interface Contract + Stub** (Risk: 2, Dependency)
   - Justification: Define interface contract `processPayment(booking_id, amount, user_payment_method) → {status: success | failed, transaction_id}`. Implement stub that always returns success in development. Allows booking flow to proceed without real payments.

5. **Booking Flow** (Risk: 2, Dependency)
   - Justification: Core user journey. Can now build against stubbed payment interface. Unblocked by payment contract definition.

6. **Provider Onboarding** (Risk: 3, Novelty)
   - Justification: Multi-step approval workflow. Can build in parallel with Booking.

7. **Admin Review Tool (Minimal)** (Risk: 2, Novelty)
   - Justification: Simple approval interface. Build in parallel.

8. **Search & Browse** (Risk: 3, Scale)
   - Justification: Scale risk can be tested later. Build now for functional search.

9. **Review System** (Risk: 1)
   - Justification: Low risk, depends only on Booking. Build now.

10. **Cancellation Flow** (Risk: 3, Novelty, Dependency)
    - Justification: Depends on Booking having happened. Can build with stubbed payment for refund logic.

11. **Notification System** (Risk: 1, Integration)
    - Justification: Well-understood email integration. Build in parallel.

12. **Dispute Resolution** (Risk: 2, Novelty)
    - Justification: Escalation workflow. Build now.

13. **Admin Dashboard (Full)** (Risk: 2, Dependency)
    - Justification: Analytics and dispute management. Build last as enhancement.

14. **Payment Integration (BLOCKED - waiting on client Stripe account)** (Risk: 5, Integration)
    - Justification: Real Stripe integration, webhooks, commission split, refund processing. Blocked until client sets up business infrastructure. Will swap stub for real implementation when unblocked.

## PM Escalation Message

"Payment processing is blocked — the client has no Stripe account or merchant entity set up. We are stubbing the payment interface so development continues, but real payment testing is blocked until the client resolves this. Can you get us a timeline?"

## Team Work While Payments Blocked

- Booking system builds against stubbed payment interface
- Provider dashboards, search, reviews - none blocked by payments
- High-risk items (real-time availability, multi-city data model) move up in priority since team has bandwidth
- When business blocker resolves, payment integration moves back to top of queue

## Key Insight

A blocked item should never stop an entire team. Dependency mapping and interface contracts let work continue around blockers. When the business blocker resolves, we swap the stub for real implementation with zero disruption to dependent systems.
