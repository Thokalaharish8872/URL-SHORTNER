# Module 4 Reflection: Postmortems & Blameless Culture

## Comprehension Questions

1. **What core problem does this module solve in incident postmortems?**
   This module solves the problem of postmortems that assign blame to individuals instead of identifying systemic failures. Blame-heavy postmortems discourage reporting, hide near-misses, and fail to prevent future incidents because they focus on "who did this" instead of "what in the system allowed this to happen."

2. **Which decision in this module has the biggest impact, and why?**
   The five-whys vs timeline-based format decision has the biggest impact because it determines whether the analysis drills down to systemic root causes or gets lost in chronological details. Five-whys forces depth and focus on root cause, while timeline can bury the most important information under pages of "what happened next."

3. **What evidence proves the implementation works end-to-end?**
   The fixed postmortem (postmortem_order_failure_fixed.md) demonstrates the implementation works: it has no individual names, root cause focuses on systemic failures (error handling, config validation, monitoring gap), all action items are system changes with specific owners/deadlines/definitions of done, and the tone is investigative not punitive.

## Mini Practical Task

**STEP 4 verification for postmortem_order_failure_fixed.md:**

**Root cause section excerpt:**
"The root cause is the combination of three systemic failures: 1. Error handling design that masks critical failures... 2. Missing config schema validation... 3. Monitoring gap between service health and business health..."

**Change made:** Removed all individual names from root cause section and focused on systems/processes. Changed from "John removed a config field" to "The deployment pipeline does not validate config changes against service requirements." This shift from individual blame to systemic analysis makes the postmortem actionable for preventing future incidents.
