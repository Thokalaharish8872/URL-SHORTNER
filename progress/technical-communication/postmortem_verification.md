# Postmortem Verification

## Root Cause Check

**Does it name a person or a system?**
System. The root cause names three systemic failures:
1. Config schema validation gap
2. Monitoring gap
3. Rollback testing gap

No individuals named in root cause section.

## The "Be More Careful" Trap Check

**Are action items system changes or human behavior changes?**
All action items are system changes:
- Add config schema validation to deployment pipeline (system)
- Add order creation rate monitoring dashboard (system)
- Update error handling to fail fast on critical failures (system)
- Test rollback automation after infrastructure changes (system)
- Align staging config schema with production (system)
- Add integration test for order persistence (system)

No "be more careful" or human behavior changes.

## Monitoring Specificity Check

**Is the monitoring action item specific enough?**
Yes. "Add order creation rate monitoring dashboard" with definition of done: "Dashboard widget showing orders-per-minute is live and alerting on zero for >5 minutes." An engineer could implement this tomorrow.

## Red Flags Check

- Root cause names an individual? ❌ No - names systems only
- Action items are "be more careful"? ❌ No - all are system changes
- Monitoring improvement is vague? ❌ No - specific with alert thresholds
- No contributing factors listed? ❌ No - 4 contributing factors listed
- Lessons learned empty or generic? ❌ No - specific insights
- Action items without owners/deadlines/definitions? ❌ No - all have all three

All checks pass.
