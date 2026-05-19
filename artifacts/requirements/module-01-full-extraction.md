# Module 1 Full Requirements Extraction - SkillSwap

## USER - Functional Requirements

1. Browse providers by category
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: High

2. View provider profiles with ratings
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: High

3. Book time slots
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: High

4. Pay through the platform
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: High

5. Cancel bookings with provider's cancellation policy applied
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: BLOCKED - pending PM decision
   - Note: Contradiction between original spec (provider autonomy) and updated spec (platform universal 24-hour rule). See module1_fix.md for two resolution options.

6. Receive confirmation emails
   - Type: Functional
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: High

## USER - Quality Attributes

7. Search must "feel instant"
   - Type: Quality Attribute
   - Stakeholder: User
   - Source: Paragraph 1, Explicit
   - Confidence: Low (latency threshold unspecified)

## PROVIDER - Functional Requirements

8. Set own availability
   - Type: Functional
   - Stakeholder: Provider
   - Source: Paragraph 2, Explicit
   - Confidence: High

9. Set own pricing
   - Type: Functional
   - Stakeholder: Provider
   - Source: Paragraph 2, Explicit
   - Confidence: High

10. Set own descriptions
    - Type: Functional
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: High

11. View bookings
    - Type: Functional
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: High

12. View earnings
    - Type: Functional
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: High

13. View reviews
    - Type: Functional
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: High

## PROVIDER - Constraints

14. Platform takes 15% commission on earnings
    - Type: Constraint
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: Medium (unclear if uniform across categories)

15. No-show users can be flagged
    - Type: Constraint
    - Stakeholder: Provider
    - Source: Paragraph 2, Explicit
    - Confidence: Medium (flagging criteria unspecified)

## PLATFORM/OPS - Functional Requirements

16. Vet new providers before approval
    - Type: Functional
    - Stakeholder: Platform/Ops
    - Source: Paragraph 2, Explicit
    - Confidence: High

17. Resolve disputes between users and providers
    - Type: Functional
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: High

18. Handle escalated disputes
    - Type: Functional
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: High

19. Approve providers
    - Type: Functional
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: High

## PLATFORM/OPS - Constraints

20. Expand to 5 cities within 6 months
    - Type: Constraint
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: High

## PLATFORM/OPS - Quality Attributes

21. Handle at least a few thousand users in one city
    - Type: Quality Attribute
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: Low ("few thousand" is vague)

22. Analytics on everything
    - Type: Quality Attribute
    - Stakeholder: Platform/Ops
    - Source: Paragraph 3, Explicit
    - Confidence: Low ("everything" is ambiguous)

## Ambiguities and Open Questions

1. **Search latency definition:** "Feel instant" is subjective. What is the specific latency threshold (e.g., <200ms, <500ms, <1s) and under what load conditions (e.g., 1000 concurrent users)? Without a number, this is a wish, not a testable requirement.

2. **Cancellation policy money flow:** If a user books and pays $100, and provider's policy says "50% refund if canceled within 24 hours" - who initiates the refund? Is it automatic? Does provider approve? Does platform eat processing fees on refund, or does the user? This phrase hides an entire payment flow.

3. **Vetting process details:** Is vetting document verification (ID, licenses), background checks, service description quality review, or in-person interview? Automated or manual? What happens to rejected providers - can they reapply? Called out as a feature but specified at zero depth.

4. **Analytics scope:** "Analytics on everything" could mean Google Analytics page tracking (a day of work) or a full data warehouse with real-time dashboards for user behavior, booking funnels, provider performance, revenue by city, cohort analysis (months of work). The word "everything" is doing the work of a 50-page analytics spec.

5. **Commission structure:** Does the 15% commission apply uniformly to all service categories, or does it vary by category or provider tier?

6. **Cancellation policy format:** How are provider cancellation policies structured? Free-text descriptions, or structured rules (e.g., "full refund if canceled 24+ hours before")?

7. **Scale target:** "At least a few thousand users" is vague. What is the specific target (e.g., 2,000, 5,000, 10,000 users) and is this per city or total across all cities?

8. **Authentication/authorization:** The spec mentions "users" and "providers" but never mentions login, signup, or account management. Are users and providers separate accounts? Can someone be both?

9. **Platform support:** Is this a web app, mobile app, or both? What platforms need to be supported initially?

10. **Notification channels:** Confirmation emails are mentioned, but what about other notifications (push, SMS, in-app)? What about appointment reminders?

11. **Provider payout timing:** When and how do providers receive their earnings (85% after commission)? Daily, weekly, monthly? What payment methods?

12. **Category management:** Who creates and manages service categories? Are they fixed or can providers create their own?

## Affected Requirements (Cancellation Decision Impact)

The cancellation policy decision affects these requirements:

- Requirement 5 (Cancel bookings) - BLOCKED pending decision
- Requirement 4 (Pay through platform) - Payment flow must handle refunds according to chosen policy
- Requirement 12 (View earnings) - Provider earnings display must account for commission and refunds
- Requirement 9 (Set own pricing) - If Option 1 chosen, providers cannot set cancellation terms, reducing pricing autonomy
- Requirement 16 (Vet new providers) - May need to verify provider cancellation policies if Option 2 chosen
