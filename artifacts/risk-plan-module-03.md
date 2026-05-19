# Module 3: Risk-Based Build Plan - SkillSwap

## Part 1: Risk Annotations (13 work items)

1. **User Authentication** - Risk: 2, Type: Dependency
   - Well-understood pattern, libraries exist. But high dependency - almost everything depends on it.

2. **Listings Data Model** - Risk: 2, Type: Dependency
   - Foundation for booking and search. Standard schema design but lasting consequences.

3. **Provider Onboarding** - Risk: 3, Type: Novelty
   - Multi-step approval process with state management. Not technically hard but easy to get wrong if states aren't clearly defined.

4. **Availability Management** - Risk: 4, Type: Novelty
   - Real-time conflict detection is a concurrency problem. Race conditions are subtle and hard to test.

5. **Search & Browse** - Risk: 3, Type: Scale
   - Works fine with small datasets, risk emerges at scale. "Feel instant" is vague performance requirement.

6. **Booking Flow** - Risk: 2, Type: Dependency
   - Standard booking logic, but depends on auth and data model. Moderate complexity.

7. **Payment Processing** - Risk: 5, Type: Integration
   - Depends on Stripe's API, webhooks, 15% commission split, refund logic. External dependency we don't control. Could invalidate entire plan if it doesn't work.

8. **Review System** - Risk: 1, Type: None significant
   - Standard CRUD pattern. Low uncertainty.

9. **Admin Review Tool (Minimal)** - Risk: 2, Type: Novelty
   - Simple approval interface. Low complexity but new workflow.

10. **Admin Dashboard (Full)** - Risk: 2, Type: Dependency
    - Analytics, dispute management. Depends on having data to display.

11. **Notification System** - Risk: 1, Type: Integration
    - Email service integration. Well-understood pattern.

12. **Cancellation Flow** - Risk: 3, Type: Novelty, Dependency
    - Refund logic depends on payment processing. Cancellation policy enforcement is new logic.

13. **Dispute Resolution** - Risk: 2, Type: Novelty
    - Escalation workflow. Moderate complexity but straightforward.

## Part 2: Ordered Build Plan

1. **User Authentication** (Risk: 2, Dependency)
   - Justification: Required by almost everything. Low risk but unblocks the most work. Build first to maximize parallelism later.

2. **Listings Data Model** (Risk: 2, Dependency)
   - Justification: Foundation for booking, search, and provider management. Build early to unblock dependent work.

3. **Availability Management** (Risk: 4, Novelty)
   - Justification: High novelty risk (concurrency). Depends only on Listings Data Model. Build early to surface race condition problems before they block booking flow.

4. **Payment Processing Spike** (Risk: 5, Integration)
   - Justification: HIGHEST RISK item. External dependency (Stripe). 2-hour throwaway proof-of-concept to verify API works, handles commission, processes refunds. If this fails, redesign entire approach before investing further.

5. **Booking Flow** (Risk: 2, Dependency)
   - Justification: Depends on Auth, Listings, Availability. Core user journey. Build now that dependencies are met and payment spike confirmed feasible.

6. **Provider Onboarding** (Risk: 3, Novelty)
   - Justification: Multi-step approval workflow. Can build in parallel with Booking since both depend on Auth and Listings.

7. **Admin Review Tool (Minimal)** (Risk: 2, Novelty)
   - Justification: Simple approval interface. Build in parallel - unblocks provider onboarding.

8. **Search & Browse** (Risk: 3, Scale)
   - Justification: Depends on Listings. Scale risk can be tested later. Build now to have functional search.

9. **Review System** (Risk: 1)
   - Justification: Low risk, depends only on Booking having happened. Build now.

10. **Cancellation Flow** (Risk: 3, Novelty, Dependency)
    - Justification: Depends on Payment Processing (completed after spike). Build now to handle refund logic.

11. **Notification System** (Risk: 1, Integration)
    - Justification: Well-understood email integration. Can build in parallel with other low-risk items.

12. **Dispute Resolution** (Risk: 2, Novelty)
    - Justification: Escalation workflow. Depends on Cancellation and Reviews having data. Build now.

13. **Admin Dashboard (Full)** (Risk: 2, Dependency)
    - Justification: Analytics and dispute management. Depends on having data from multiple systems. Build last as it's a nice-to-have enhancement over the minimal review tool.

## Top 3 Highest-Risk Items

1. Payment Processing (Risk: 5, Integration)
2. Availability Management (Risk: 4, Novelty)
3. Provider Onboarding (Risk: 3, Novelty) OR Search & Browse (Risk: 3, Scale) OR Cancellation Flow (Risk: 3, Novelty, Dependency)
