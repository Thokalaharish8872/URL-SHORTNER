# Postmortem: Order Processing Failure (Blameless Version)

## Summary

At 14:00 on [date], OrderProcessor v2.14 was deployed to production. The deployment removed a config field (`warehouse_routing`) that the running service still required. The service's error handling caught the missing field exception, logged a warning at DEBUG level, and returned 200 OK to clients without persisting orders. Over 34 minutes, 1,400 orders were dropped while the service appeared healthy. Incident was resolved at 16:02 after manual rollback to v2.13. Total downtime: 1 hour 2 minutes.

## Five-Whys Analysis

**Why were customers charged but orders were not created?**
The service's error handling strategy uses a broad try/except block around the order creation path. This design was implemented to prevent service crashes on non-critical errors, but it also masks critical failures like missing required fields by returning success responses.

**Why did the service catch the error silently instead of failing fast?**
The error handling policy prioritizes service availability over data integrity. Errors are logged at DEBUG level instead of ERROR level, and the service returns 200 OK even when critical operations fail. This design choice was made without considering the impact on business-critical operations like order persistence.

**Why was the missing config field not caught before deployment?**
The deployment pipeline does not validate config changes against service requirements. The staging environment uses a different config schema than production, so the missing field was not caught in staging. There is no automated check that verifies a config field is not being removed while any running service version still references it.

**Why did the monitoring not detect the order processing failure?**
The monitoring system measures service health (HTTP response codes, latency, CPU, memory) but does not measure business health (order creation rate). There is no alerting threshold for "orders per minute dropping to zero." The dashboard showed all green because the service was returning 200 OK, even though it was failing to perform its primary function.

**Why did the rollback fail?**
The rollback automation script references an old deployment artifact path that no longer exists after the infrastructure migration 4 months ago. There is no requirement to test rollback automation after infrastructure changes, and no automated verification that rollback scripts remain functional.

## Root Cause

The root cause is the combination of three systemic failures:

1. **Error handling design that masks critical failures:** The service's broad try/except block returns success responses even when order persistence fails. This design choice made the config field removal dangerous because the service did not fail visibly.

2. **Missing config schema validation:** There is no automated validation in the deployment pipeline that checks whether config changes maintain backward compatibility with running service versions. The system allows destructive config changes without verification.

3. **Monitoring gap between service health and business health:** The monitoring system validates that the service is running and responding quickly, but does not validate that the service is actually performing its business function (creating orders). This gap made the silent data loss invisible to automated monitoring.

The config field removal was the trigger, but the system design made it possible for that trigger to cause silent data loss without any automated detection.

## Contributing Factors

1. **Escalation procedure does not distinguish between service failures and business failures:** The escalation process treats all customer-reported issues through the same triage path. The initial assumption that the issue was an email delivery delay (based on past patterns) delayed investigation by 15 minutes.

2. **Staging-production config drift:** The staging environment uses a different config schema than production. Staging never had the `warehouse_routing` field in its config, so the missing field was not caught in staging. This reduces the effectiveness of staging as a validation environment.

3. **Untested rollback automation after infrastructure changes:** The infrastructure migration 4 months ago changed deployment artifact paths, but there is no requirement to re-test rollback automation after such changes. This led to a stale rollback script that failed when needed.

4. **Integration test validates service response but not data persistence:** The automated test suite validates that the service returns 200 OK but does not validate that orders are actually written to the database. This test gap allows the service to pass all checks while failing to perform its primary function.

## Action Items

| Description | Owner | Deadline | Definition of Done |
|-------------|-------|----------|-------------------|
| Add backwards-compatibility check to CI pipeline that fails the build if a config field is removed while any running service version still references it | Platform team lead | 2 weeks | CI pipeline has automated config-diff analysis that flags removed or renamed fields; build fails if field is referenced in service code |
| Add orders-per-minute metric with alert that fires when rate drops below trailing-7-day average by more than 50% for 5 minutes | Observability team lead | 1 week | Dashboard widget shows orders-per-minute; alert configured and tested; alert fires to #ops-alerts channel |
| Update error handling to fail fast on critical failures (missing required fields, database failures) | Backend team lead | 1 week | Critical errors return 500 instead of 200; errors logged at ERROR level; tests verify failure behavior |
| Add rollback dry-run step to deploy pipeline and audit rollback scripts monthly | Deployment team lead | Immediate | Deploy pipeline includes rollback dry-run; monthly audit scheduled; rollback scripts tested in staging environment |
| Align staging config schema with production | QA team lead | 1 week | Staging environment uses same config schema as production with test data values; config comparison test added to CI |
| Add integration test that validates order persistence to database | QA team lead | 2 weeks | Automated test creates order and verifies it exists in database; test runs on every deploy |

## Lessons Learned

**What surprised the team:**
The service could return 200 OK while completely failing to perform its primary function (persisting orders). The team assumed HTTP 200 meant success, but the broad error handling made this assumption false.

**What worked well:**
The decision to check the order database directly when monitoring showed green was the breakthrough that identified the root cause. Bypassing the misleading service health metrics and checking business state directly provided the critical information.

**What the team would do differently:**
If the same incident happened tomorrow before action items are completed, the team would:
1. Check business metrics (order creation rate) immediately, not just service health metrics
2. Assume service health metrics are misleading until proven otherwise
3. Escalate to platform team immediately if automated rollback fails, rather than attempting manual intervention first
4. Verify rollback automation after any infrastructure change, regardless of how minor the change appears
