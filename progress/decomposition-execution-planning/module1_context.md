# Module 1 Context: Requirements Analysis

## Micro-Exercise: Assumptions in "Users can book time slots and pay through the platform"

**Assumptions hiding in this sentence:**

1. **Time slot definition:** Fixed duration (1 hour)? Variable length set by provider? Multiple slots per booking? Minimum/maximum duration constraints?

2. **Booking behavior:** Reserve now pay later? Pay immediately to confirm? Hold period while user decides? What happens on double-book attempts?

3. **Payment methods:** Credit card only? Multiple methods (PayPal, Apple Pay)? Does platform hold money and pay provider later, or pass through directly? What currency? What if payment fails after reservation?

4. **User identity:** Authenticated users only? Can guests browse but not book? Is account creation required before booking?

5. **Confirmation flow:** Real-time auto-confirmation on payment? Does provider need to confirm? What if provider hasn't updated calendar and is actually unavailable?

6. **Time zone handling:** All in provider's time zone? User's time zone? Displayed in local time for both?

7. **Cancellation policy:** Can users cancel? With refund? Partial refund? What happens to time slot after cancellation?

One sentence, at least 7 major assumptions. This demonstrates why reading requirements requires finding what's missing, not just what's written.
