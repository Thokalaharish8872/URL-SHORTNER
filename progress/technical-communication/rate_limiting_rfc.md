# RFC: Add Rate Limiting to Public API

## Problem Statement

Over the past month, a single customer accidentally sent 50,000 requests per minute, degrading response times for all users. The on-call engineer had to manually block the customer at 2 AM by editing config files and redeploying. The product team wants to launch a paid tier with guaranteed rate limits, but we have no rate limiting infrastructure to build on.

**Business impact:** Service degradation affects customer trust and revenue. Manual intervention at 2 AM is unsustainable. Paid tier launch is blocked.

## Proposed Approach

Add a distributed rate limiter at the API gateway using the token bucket algorithm with Redis as the shared counter store.

**Where it sits:** API gateway (front door) before requests reach application servers.

**Algorithm:** Token bucket. Each customer has a token bucket that refills at a steady rate. Requests consume tokens; if the bucket is empty, the request is rejected with HTTP 429.

**Storage:** Redis (shared data store) for counters across all gateway instances. This ensures consistent limits regardless of which instance handles the request.

**Implementation:**
1. Redis cluster (3 nodes) for high availability
2. Token bucket middleware in the gateway
3. Admin API for configuring per-customer limits
4. Dashboard for monitoring rate limit violations

## Alternatives Considered

**Alternative 1: Fixed-window rate limiting in application code**
- Count requests per minute per customer, reset at the top of each minute
- Store counters in local memory on each application server
- Pros: Simple to implement, no Redis dependency
- Cons: Doesn't work across multiple servers, bursty traffic at minute boundaries, no centralized admin

**Alternative 2: Third-party rate limiting service (e.g., Cloudflare, AWS API Gateway)**
- Offload rate limiting to a CDN or cloud provider
- Pros: No infrastructure to maintain, scalable, built-in dashboards
- Cons: Vendor lock-in, additional cost, less control over custom logic for paid tiers

## Risks and Mitigations

**Risk 1: Redis failure breaks rate limiting**
- Mitigation: Redis cluster with automatic failover. If Redis is down, rate limiter fails open (allows all requests) to avoid breaking legitimate traffic.

**Risk 2: Incorrect limit configuration for paid tiers**
- Mitigation: Limits must be configured via admin API with approval workflow. Dashboard shows real-time usage vs limits.

**Risk 3: Performance overhead from Redis calls on every request**
- Mitigation: Use Redis pipeline for batched operations. Load test to ensure <10ms overhead. Consider local caching for high-volume customers.

**Risk 4: Doing nothing**
- Impact: Continued service degradation, manual intervention required, paid tier blocked. Another incident could cause customer churn.

## Open Questions

1. **What are the specific rate limits for each tier?** Product team needs to define limits for free, pro, and enterprise tiers.

2. **How do we handle burst traffic for legitimate spikes?** Token bucket allows bursts, but we need to define bucket size vs refill rate ratios.

3. **Do we rate limit by API key or by IP address?** API keys are more accurate for multi-tenant customers, but IP-based limits prevent abuse without keys.

4. **What is the rollout plan?** Should we enable rate limiting gradually, starting with abusive customers only?
