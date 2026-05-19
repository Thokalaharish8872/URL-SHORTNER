# Module 5: Failure Mode Analysis

## Failure Mode Table

| Dependency | Failure Mode | Probability | User Impact | Current Handling | Desired Handling |
|---|---|---|---|---|---|
| Database | Connection refused (database down) | Medium | Complete service outage - all reads and writes fail | Unhandled - service crashes or returns unstructured 500 | Return 503 with "service temporarily unavailable", retry connection with backoff |
| Database | Slow queries (database up but slow) | High | Requests hang, timeouts cascade, users see spinners | No query timeout - waits indefinitely | Query timeout of 5 seconds, return 504 if exceeded, log slow query |
| Cache (Redis) | Down (unreachable) | Medium | Every request hits database - slower responses, possible overload | Crashes or throws unhandled error | Fall through to database, log warning, degrade gracefully |
| Cache (Redis) | Stale data (outdated info) | High | Users see old data - minor or critical depending on data | Not detected | TTL-based expiry, cache-aside pattern, version stamps |
| Email API (SendGrid) | Down (unreachable) | Medium | Email notifications fail, SMS/push still work | Throws error, returns 500 | Circuit breaker, queue for retry, return success after queuing |
| Email API (SendGrid) | Slow (high latency) | High | Service becomes as slow as slowest dependency | No timeout, waits indefinitely | Strict timeout (5s), circuit breaker, cached fallback |
| SMS API (Twilio) | Down (unreachable) | Medium | SMS notifications fail, email/push still work | Throws error, returns 500 | Circuit breaker, queue for retry, log warning |
| SMS API (Twilio) | Slow (high latency) | High | Service becomes as slow as slowest dependency | No timeout, waits indefinitely | Strict timeout (5s), circuit breaker, cached fallback |
| Push API (Firebase) | Down (unreachable) | Medium | Push notifications fail, email/SMS still work | Throws error, returns 500 | Circuit breaker, queue for retry, log warning |
| Push API (Firebase) | Slow (high latency) | High | Service becomes as slow as slowest dependency | No timeout, waits indefinitely | Strict timeout (5s), circuit breaker, cached fallback |
| Disk | Full (no available space) | Low-Medium | Logs stop writing, database may crash, uploads fail | Silent failure - no logs about failing to write logs | Disk usage metric with alert at 80%, log rotation, temp file cleanup |
| Memory | OOM (exceeds available memory) | Low-Medium | Process killed by OS - immediate crash, requests lost | Process dies, container restarts | Memory limit in container, heap usage metric, alert at 80% |
| Database | Connection pool exhaustion | Medium | Database fine but all pool slots taken by slow queries | Requests hang waiting for pool slot | Pool timeout (5s), alert on pool usage > 80%, max connections limit |
| Network | Partition (partial connectivity) | Low | Can reach some dependencies but not others | Reads work, writes fail if primary unreachable | Circuit breakers per dependency, fallback to read replicas |
| DNS | Resolution failure (hostname doesn't resolve) | Low | Hostnames don't resolve, cryptic errors (ENOTFOUND, getaddrinfo failed) everywhere | Cryptic "connection refused" or "host not found", hard to diagnose | DNS health check, cached IPs with TTL, alert on DNS failures, meaningful error messages |

## Risk Surface
**Current Handling Analysis**: 12 of 15 entries show "crash", "hang", or "unhandled" - this is the risk surface where the service will completely fail with no graceful behavior.

## Simulations

### Simulation 1: Database Stopped
- **Expected Behavior**: Service returns 503 immediately
- **Actual Behavior**: Service hangs for 30s then returns 500
- **Gap**: No timeout configured on database connection

### Simulation 2: 1ms Timeout on External API
- **Expected Behavior**: Request fails fast with clear error
- **Actual Behavior**: Request throws unhandled exception, returns 500
- **Gap**: No error handling for timeout exceptions
