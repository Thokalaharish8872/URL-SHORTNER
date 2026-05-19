# Module 3 Break: Business Blocker Analysis

## Risk Type Analysis

This is **not a technical risk** - it does not fit into the four categories (integration, novelty, dependency, scale). This is a **business/legal risk** - a condition that must exist outside the codebase for the feature to be possible at all.

The four risk categories I defined are all about what could go wrong IN the code or architecture. But projects also face:
- Business risks (no merchant account, no business entity)
- Legal risks (compliance, regulations)
- Organizational risks (team changes, leadership changes)
- People risks (key person dependency)

A mature planner asks not just "can we build this?" but "are the conditions in place for this to even be possible?"

## Impact on Risk-Ordered Plan

My plan had Payment Processing as item 4 (after the spike). Now:
- I cannot build Payment Processing at all until the client sets up business infrastructure
- The spike (2-hour Stripe proof-of-concept) is also blocked - no Stripe account to test with
- This changes the plan from a technical blocking issue to a business blocking issue

## Can Progress Continue While Payments Blocked?

Yes, I can make progress on almost everything else:
- Auth, Listings Data Model, Availability Management - no payment dependency
- Booking Flow - can be built with a mock payment interface or "pay on arrival" mode
- Search & Browse, Reviews, Notifications - no payment dependency
- Admin tools - no payment dependency

The booking flow is the only item that directly depends on payments. I can build the entire booking UX, time slot selection, and confirmation flow with a mock payment step, then wire in real payments once the business infrastructure is ready.

**Key insight:** This is not my problem to solve (setting up merchant account), but it IS my problem to plan around by building the rest of the system while the business side resolves their blocker.
