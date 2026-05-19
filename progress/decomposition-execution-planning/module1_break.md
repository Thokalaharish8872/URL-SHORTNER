# Module 1 Break: Spec Contradiction

## Contradiction Identified

**Original Paragraph 1:** "...cancel bookings with the provider's cancellation policy applied."

**Updated Paragraph 1:** "all cancellations made within 24 hours of booking receive a full refund, regardless of the reason. Cancellations after 24 hours are non-refundable."

**Paragraph 2:** "Providers set their own availability, pricing, and service descriptions."

## The Conflict

The spec now contains two different cancellation systems that cannot coexist:

1. **Provider autonomy:** Original spec says providers set their own cancellation policies, and those policies apply when users cancel. This implies providers can define rules like "full refund up to 48 hours, 50% up to 24 hours, nothing after."

2. **Platform uniformity:** Updated spec enforces a universal rule: ALL cancellations within 24 hours get full refund, no exceptions. Cancellations after 24 hours are non-refundable, period.

## Why This Matters

These cannot both be true. If providers set their own policies (maybe more generous than the platform rule), but the platform also enforces a strict universal rule, which one applies?
- Does provider policy override platform rule?
- Does platform rule override provider policy?
- What if provider's policy is MORE generous than the platform rule?

This is a realistic scenario where different stakeholders write different parts of a spec, and nobody checks for consistency across sections.
