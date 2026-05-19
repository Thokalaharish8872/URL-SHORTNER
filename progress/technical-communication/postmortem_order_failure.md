# Postmortem: Order Processing Failure

## Summary

At 14:00 on [date], OrderProcessor v2.14 was deployed to production. The service began silently failing to persist orders while returning 200 OK to clients. Over 34 minutes, 1,400 orders were dropped. Customers were charged by the payment processor but received no confirmation emails. Incident was resolved at 16:02 after manual rollback to v2.13. Total downtime: 1 hour 2 minutes.

## Five-Whys Analysis

**Why were customers charged but orders were not created?**
OrderProcessor v2.14 removed the `warehouse_routing` field from the config. The service caught the missing field error in a broad try/except block, logged a warning at DEBUG level, and returned 200 to the client without writing the order to the database.

**Why did the service catch the error silently instead of failing fast?**
The error handling strategy uses a broad try/except block around the order creation path. This design choice was made to prevent the service from crashing on non-critical errors, but it also masks critical failures like missing required fields.

**Why was the missing config field not caught before deployment?**
The staging environment uses a different config schema than production. Staging never had the `warehouse_routing` field in its config, so the missing field was not caught in staging. The integration tests do not validate the config schema against production requirements.

**Why did the monitoring not detect the order processing failure?**
The monitoring system checks only HTTP response codes and latency. It does not check whether orders are actually being created. There is no alerting threshold for "orders per minute dropping to zero."

**Why did the rollback fail?**
The rollback automation has not been tested since the infrastructure migration 4 months ago. The rollback script references an old deployment artifact path that no longer exists after the migration.

**Why was the infrastructure migration not followed by testing the rollback automation?**
There is no requirement in the deployment checklist to verify rollback procedures after infrastructure changes. The testing of rollback automation is considered a "nice to have" rather than a required validation step.

## Root Cause

The root cause is the combination of three systemic failures:
1. **Config schema validation gap:** There is no automated validation that production config changes maintain backward compatibility with service requirements
2. **Monitoring gap:** The monitoring system measures service health (HTTP codes, latency) but not business health (order creation rate)
3. **Rollback testing gap:** There is no requirement to test rollback automation after infrastructure changes, leading to stale automation that fails when needed

The config field removal was the trigger, but the system made it possible for that trigger to silently drop 1,400 orders without any automated detection.

## Contributing Factors

1. **Escalation process delay:** The escalation process did not distinguish between email delivery delays and order processing failures. The on-call engineer assumed the issue was an email delay based on past experience, delaying investigation by 15 minutes.
2. **Broad error handling:** The try/except block that catches all exceptions prevents the service from crashing but also masks critical failures. Errors are logged at DEBUG level instead of WARNING or ERROR.
3. **Staging-production config drift:** Staging and production use different config schemas, reducing the effectiveness of staging as a validation environment.
4. **No integration test for order persistence:** The automated test suite validates that the service returns 200 OK but does not validate that orders are actually written to the database.

## Action Items

| Description | Owner | Deadline | Definition of Done |
|-------------|-------|----------|-------------------|
| Add config schema validation to deployment pipeline | Platform team lead | 2 weeks | Deployment pipeline validates config changes against service requirements before allowing deploy to production |
| Add order creation rate monitoring dashboard | Observability team lead | 1 week | Dashboard widget showing orders-per-minute is live and alerting on zero for >5 minutes |
| Update error handling to fail fast on critical failures | Backend team lead | 1 week | Critical errors (missing required fields, database failures) return 500 instead of 200 and are logged at ERROR level |
| Test rollback automation after infrastructure changes | Deployment team lead | Immediate | Deployment checklist updated to require rollback test after any infrastructure change |
| Align staging config schema with production | QA team lead | 1 week | Staging environment uses same config schema as production with test data values |
| Add integration test for order persistence | QA team lead | 2 weeks | Automated test validates that orders are written to database, not just that service returns 200 |

## Lessons Learned

**What surprised the team:**
The service could return 200 OK while completely failing to perform its primary function (persisting orders). The team assumed HTTP 200 meant success, but the broad error handling made this assumption false.

**What worked well:**
The on-call engineer's decision to check the order database directly when monitoring showed green was the breakthrough that identified the root cause. Direct database inspection bypassed the misleading service health metrics.

**What the team would do differently:**
If the same incident happened tomorrow before action items are completed, the team would:
1. Check business metrics (order creation rate) immediately, not just service health metrics
2. Assume service health metrics are misleading until proven otherwise
3. Escalate to platform team immediately if automated rollback fails, rather than attempting manual intervention first
