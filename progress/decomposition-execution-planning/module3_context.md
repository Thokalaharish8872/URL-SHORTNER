# Module 3 Context: Risk-Based Ordering

## Micro-Exercise: Rank Tasks by Risk

**Ranking (most risky to least risky):**

1. **Integrate third-party payment API (Stripe)** - HIGHEST RISK
   - External dependency outside my control
   - Unfamiliar territory (webhooks, idempotency, test modes)
   - Rate limits or API design could invalidate entire plan
   - If it doesn't work, the product cannot exist

2. **Design database schema for provider profiles** - MEDIUM RISK
   - I control it, but design choices have lasting consequences
   - Schema changes are expensive once data exists
   - Migration complexity if design is wrong

3. **Build CRUD form for user profile editing** - LOWEST RISK
   - Well-understood pattern I've done many times
   - Easily changed if needed
   - No unknowns or external dependencies
   - Could take more time than payment API but is not risky

**Key insight:** Risk is not about difficulty or time - it's about unknowns and external dependencies. The CRUD form might take longer but I know exactly how to build it. The payment API might be simple but has unknowns that could invalidate the entire plan.
