# Flawed Runbook Analysis

## Failure 1: Stale Environment Variable Name

**Location:** Step 3, line: `kubectl exec -n production deployment/orderflow-api -- python -c "import psycopg2; psycopg2.connect('$DB_CONNECTION_STRING')"`

**What would happen:** The on-call engineer would get a Python error saying the environment variable DB_CONNECTION_STRING doesn't exist. The service description says the variable is DATABASE_URL, not DB_CONNECTION_STRING. The engineer would waste time debugging why the connection fails, potentially escalating to the wrong team or trying to fix a configuration that doesn't exist.

**Correct fix:** Change all instances of `DB_CONNECTION_STRING` to `DATABASE_URL` to match the actual environment variable name used by the service.

## Failure 2: Rollback Command Actually Rolls Forward

**Location:** Step 6, command: `helm upgrade orderflow deploy/charts/orderflow --namespace production --set image.tag=latest`

**What would happen:** The heading says "roll back" but the command uses `helm upgrade --set image.tag=latest`, which deploys the latest image - the same image that just caused the failure. This is rolling forward, not rolling back. The on-call engineer would deploy the broken image again, potentially making the outage worse or longer. The correct command would be `helm rollback orderflow --namespace production` which rolls back to the previous stable version.

**Correct fix:** Replace `helm upgrade` with `helm rollback orderflow --namespace production` to actually roll back to the previous release.

## Failure 3: Missing Redis Check

**Location:** Entire runbook - no mention of Redis anywhere

**What would happen:** The service description states OrderFlow depends on Redis for rate limiting and as the Celery broker. If Redis is down, the background worker stops processing refunds and rate limiting is disabled. An on-call engineer following this runbook would never check Redis, so they would chase symptoms (slow responses, refunds not processing) without finding the root cause. They might restart the service or roll back deployments unnecessarily while Redis remains down, extending the incident duration.

**Correct fix:** Add a failure mode for Redis connection similar to the database failure mode, with steps to check Redis status, restart if down, and verify connectivity.
