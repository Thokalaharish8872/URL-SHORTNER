# OrderFlow On-Call Runbook

## Constants

**Service Name:** orderflow
**Namespace:** production
**API Port:** 8080
**On-call Slack:** #orderflow-oncall
**Data Engineering Slack:** #data-eng
**Platform Infrastructure Slack:** #platform-infra
**PagerDuty Policy:** OrderFlow Primary

## Tool Prerequisites

This runbook assumes the following tools are installed:
- `kubectl`: Kubernetes CLI for cluster management
- `helm`: Kubernetes package manager for deployments
- `psql`: PostgreSQL command-line client
- `redis-cli`: Redis command-line client
- `systemctl`: Linux service manager (standard on most Linux systems)
- `ps aux`: Process listing command (standard on Unix systems)

If any tool is not installed, escalate to #platform-infra for installation.

## Service Health Check

1. Check if API is responding:
   ```bash
   curl -f http://localhost:8080/health
   ```
   Expected output: `{"status":"healthy"}`

2. If health check fails, check if the service is running:
   ```bash
   ps aux | grep orderflow
   ```

3. If service is not running, restart it:
   ```bash
   systemctl restart orderflow
   ```

## Common Failure Modes

### Failure Mode 1: Database Connection Lost

**Symptoms:** API returns 500 errors, logs show "connection refused" or "timeout" to PostgreSQL

**Recovery Steps:**

1. Check database connectivity:
   ```bash
   psql $DATABASE_URL -c "SELECT 1"
   ```

2. If database is unreachable, check PostgreSQL status:
   ```bash
   systemctl status postgresql
   ```

3. If PostgreSQL is down, start it:
   ```bash
   systemctl start postgresql
   ```

4. If PostgreSQL is running but unreachable from the API:
   - Check network connectivity: `ping <database-host>`
   - Check firewall rules: `sudo iptables -L -n`
   - Escalate to #data-eng in Slack

5. After database is accessible, restart OrderFlow:
   ```bash
   systemctl restart orderflow
   ```

6. Verify health check passes:
   ```bash
   curl -f http://localhost:8080/health
   ```

### Failure Mode 2: Redis Connection Lost

**Symptoms:** API returns 503 errors, rate limiting disabled, slow responses

**Recovery Steps:**

1. Check Redis connectivity:
   ```bash
   redis-cli -u $REDIS_URL ping
   ```
   Expected output: `PONG`

2. If Redis is unreachable, check Redis status:
   ```bash
   systemctl status redis
   ```

3. If Redis is down, start it:
   ```bash
   systemctl start redis
   ```

4. If Redis is running but unreachable:
   - Check network connectivity: `ping <redis-host>`
   - Escalate to #platform-infra in Slack

5. After Redis is accessible, restart OrderFlow:
   ```bash
   systemctl restart orderflow
   ```

6. Verify health check passes:
   ```bash
   curl -f http://localhost:8080/health
   ```


### Failure Mode 3: Background Worker Stopped Processing

**Symptoms:** Refund requests not processing, refund queue growing

**Recovery Steps:**

1. Check if Celery worker is running:
   ```bash
   ps aux | grep celery
   ```

2. If worker is not running, start it:
   ```bash
   cd /path/to/orderflow/repo
   celery -A orderflow.worker worker --loglevel=info
   ```

3. Check queue length:
   ```bash
   redis-cli -u $CELERY_BROKER_URL LLEN celery
   ```

4. If queue length is > 1000, escalate to #orderflow-oncall in Slack for additional worker instances

5. Monitor queue draining:
   ```bash
   watch -n 5 'redis-cli -u $CELERY_BROKER_URL LLEN celery'
   ```

### Failure Mode 4: API Returning 5xx Errors

**Symptoms:** Health check passes, but API endpoints return 500-599 errors

**Recovery Steps:**

1. Check application logs for errors:
   ```bash
   journalctl -u orderflow -f --since "5 minutes ago"
   ```

2. Check for recent deployments:
   ```bash
   helm list -n production
   kubectl rollout history deployment/orderflow -n production
   ```

3. If a recent deployment correlates with error onset, roll back:
   ```bash
   helm rollback orderflow --namespace production
   ```

4. If no recent deployment, check resource usage:
   ```bash
   kubectl top pods -n production
   ```

5. If CPU/memory is at limits, scale up:
   ```bash
   kubectl scale deployment orderflow --replicas=4 -n production
   ```

6. If resource usage is normal, escalate to #orderflow-oncall in Slack for team investigation

## Escalation Path

**When to escalate:**
- Database or Redis is down and cannot be restarted
- Queue length > 1000 and not draining
- 5xx errors persist after rollback
- Unknown failure mode not covered in this runbook

**How to escalate:**
1. Page on-call via PagerDuty (OrderFlow Primary policy)
2. Post in #orderflow-oncall Slack with:
   - Failure mode observed
   - Steps already attempted
   - Current service status
3. If no response in 15 minutes, page Platform Payments team lead

## Rollback Procedure

**When to rollback:** After recent deployment causing issues

**Steps:**

1. Identify previous stable version:
   ```bash
   helm history orderflow -n production
   ```

2. Rollback to previous version:
   ```bash
   helm rollback orderflow --namespace production
   ```

3. Verify rollback completed:
   ```bash
   kubectl rollout status deployment/orderflow -n production
   ```

4. Verify health check passes:
   ```bash
   curl -f http://localhost:8080/health
   ```

5. Post in #orderflow-oncall Slack: "Rolled back OrderFlow to version [version] due to [reason]"
