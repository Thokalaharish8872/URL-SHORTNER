# Module 1 Fix: Cancellation Contradiction Resolution

## Two Concrete Options for PM Decision

### Option 1: Platform-First Cancellation

**Policy:** The platform sets a universal cancellation policy: full refund within 24 hours of booking, non-refundable after 24 hours. Providers cannot override this policy.

**Who it affects:** Users get consistent experience across all providers. Providers lose autonomy to set their own cancellation terms.

**Tradeoff:** Simplifies user experience (one policy everywhere) but removes provider flexibility. Some providers might want stricter policies (e.g., same-day services where 24-hour window doesn't make sense) or more generous policies to attract customers.

**Implementation complexity:** Low. Single rule enforced at platform level during cancellation. Provider dashboard doesn't need cancellation policy configuration.

### Option 2: Provider Policy with Platform Floor

**Policy:** Providers set their own cancellation policies (full refund windows, partial refund tiers, no-refund periods), but the platform enforces a minimum protection: users always get at least a full refund if they cancel within 1 hour of booking (a "cooling off" period). Beyond that hour, the provider's policy applies.

**Who it affects:** Users get a safety net, providers retain autonomy to customize policies for their service type. Platform enforces a consumer protection floor.

**Tradeoff:** Preserves provider autonomy while giving users safety net. More complex to build (each provider's policy must be displayed during booking and enforced during cancellation, policy validation required).

**Implementation complexity:** High. Requires provider dashboard UI for policy configuration, policy storage in database, policy display during booking flow, policy enforcement logic during cancellation, and conflict resolution if provider policy violates platform floor.
