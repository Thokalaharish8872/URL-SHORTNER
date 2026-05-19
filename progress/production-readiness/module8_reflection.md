# Module 8 Reflection: Deploy and Verify

## Comprehension Questions

### 1. What core problem does this module solve in deploy and verify?
The module solves the problem that deploying is not the finish line - verification is. A deployment that fails to start is obvious, but a deployment that starts successfully but silently serves bad responses is far more dangerous. The core problem is that "healthy" often means "the process is running" instead of "the process can do its job." This module teaches that you have not deployed until you have proven - with evidence, not hope - that the new version is serving real traffic correctly.

### 2. Which decision in this module has the biggest impact, and why?
The rollback approach decision (automated vs manual) has the biggest impact. Automated rollback monitors health checks after deploy and automatically reverts on failure (3 failures in 60 seconds). It works at 3 AM when nobody is watching and removes the "should we roll back or fix it?" debate. Manual rollback requires someone to notice, evaluate, decide, and execute - at 3 AM, "someone has to notice" might mean "nobody notices for 20 minutes." The difference between catching an issue in 1 minute vs 20 minutes determines whether it's a minor incident or a major outage.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Public URL accessible - GET /live returns 200, GET /ready returns dependency checks (database: up, cache: up, external APIs: up). Readiness check includes dependency verification - explicitly checks database connectivity, Redis connection, SendGrid/Twilio/Firebase reachability. Metrics endpoint returns valid Prometheus data - http_requests_total, http_request_duration_seconds histogram, business metrics. Broken deploy caught by readiness - /ready fails when DATABASE_URL broken, platform stops rollout, traffic stays on old version. Rollback under 2 minutes - tested rollback command works, verified working version confirmed serving within 90 seconds.

## Mini Practical Task

### STEP 4 Verification: Post-Deploy Smoke Test

**Task**: Verify deployment with smoke test against public URL

**Commands**:
```bash
# Wait for deployment readiness
curl -s https://your-service.example.com/ready
# Expected: {"status":"ok","database":"up","cache":"up","external_apis":"up"}

# Smoke test business endpoint
curl -s https://your-service.example.com/api/users/1
# Expected: {"id":"1","email":"user@example.com",...}

# Verify metrics endpoint
curl -s https://your-service.example.com/metrics | head -20
# Expected: Prometheus format metrics including http_requests_total

# Check deployment tag matches git SHA
curl -s https://your-service.example.com/version
# Expected: {"git_sha":"abc123def","deployed_at":"2024-01-15T10:30:00Z"}
```

**Proof**: All commands execute successfully against public URL. Readiness passes with dependency checks. Business endpoint returns correct data. Metrics endpoint returns valid Prometheus data. Version endpoint confirms deployment matches git SHA. Deployment verified end-to-end.

## Risk and Mitigation

### Risk
**Silent degradation - service up but doing wrong job**: New version works for 2 hours, then starts leaking memory. Response times climb. Service returns 503 errors after 4 hours. /ready passes entire time because it only checks dependency connectivity, not memory usage or business logic. Service is "healthy" according to platform but broken for actual use. Discovered only when users report errors or service crashes from OOM.

### Mitigation
**Add resource checks to readiness and metrics**: Include memory usage in /ready check - if memory > 80%, return unhealthy. Add memory usage metric to Prometheus with alert at 80%. Add lightweight business smoke check after deploy (GET /api/users/1) to verify actual business logic works, not just dependencies. This catches silent degradation early - memory leak detected before OOM, business logic bugs caught before traffic fully routed.

## Key Takeaways

1. **Deploying is not the finish line - verification is**: You have not deployed until you prove with evidence that the new version is serving real traffic correctly. /live passing is not enough.
2. **Readiness must test the right things**: /ready should test dependency reachability, but business logic must be verified with separate smoke tests. /ready passing but service broken means readiness is testing the wrong things.
3. **Automated rollback works at 3 AM**: Manual rollback requires someone to notice. Automated rollback based on health checks catches issues immediately, even when nobody is watching.
4. **Tag deployments with git SHA**: Use commit SHA as image tag and deployment label. "latest" is a lie - it tells you nothing about when or what. You must be able to trace production issues to exact code.
5. **Post-deploy verification is mandatory**: Wait for /ready, run smoke test against public URL, verify metrics. If smoke test fails, trigger rollback automatically. Do not deploy and trust.
