# Runbook Verification

## Copy-Paste Audit

**Command 1:** `curl -f http://localhost:8080/health`
- Can paste directly: Yes
- Assumes working directory: No
- Uses environment variables: No

**Command 2:** `psql $DATABASE_URL -c "SELECT 1"`
- Can paste directly: Yes
- Assumes working directory: No
- Uses environment variables: Yes ($DATABASE_URL) - stated in service description at top

**Command 3:** `celery -A orderflow.worker worker --loglevel=info`
- Can paste directly: Yes
- Assumes working directory: Yes - not stated. FIX: Should specify working directory or that it runs from repo root

**Command 4:** `helm rollback orderflow --namespace production`
- Can paste directly: Yes
- Assumes working directory: No
- Uses environment variables: No

**Fix needed:** Add working directory for Celery worker command.

## Duplication Check

**Port 8080:** Appears in 2 places (service description, health check URL). FIX: Define at top and reference.

**PostgreSQL:** Referenced by connection string variable, not hardcoded port - good.

**Redis:** Referenced by connection string variable, not hardcoded port - good.

**Namespace "production":** Appears in 3 kubectl/helm commands. FIX: Define at top and reference.

**Slack channels:** #orderflow-oncall appears 3 times, #data-eng once, #platform-infra once. FIX: Define at top and reference.

**Service name "orderflow":** Appears in multiple commands. FIX: Define at top and reference.

## The New Hire Test

**Where would they get stuck?**
- Don't know what `ps aux` does - should explain briefly
- Don't know what `systemctl` is - should explain it's Linux service manager
- Don't know what `kubectl` is - should explain it's Kubernetes CLI
- Don't know what `helm` is - should explain it's Kubernetes package manager
- Don't know what `psql` is - should explain it's PostgreSQL CLI
- Don't know what `redis-cli` is - should explain it's Redis CLI
- Don't know what `watch` command does - should explain

**Where would they need to open a browser tab?**
- To understand what Celery is
- To understand what PagerDuty is
- To understand what journalctl is

## Red Flags Check

- Steps like "configure the database" without exact commands? ❌ No - all commands are exact
- "You will need to set up your SSH keys"? ❌ No - not mentioned
- Prose paragraphs where numbered steps should be? ❌ No - all procedural sections use numbered steps
- No escalation path? ❌ No - escalation path is clear
- Referencing tools without installation instructions? ✅ YES - kubectl, helm, psql, redis-cli, celery all referenced without installation instructions
- Mixing explanation with procedure? ✅ YES - some steps include explanation ("Note: OrderFlow continues to work without Redis...") mixed with recovery steps

## Required Fixes

1. Define constants at top (port 8080, namespace, service name, Slack channels)
2. Add working directory for Celery command
3. Add brief explanations for tools (kubectl, helm, psql, redis-cli, systemctl, ps aux)
4. Move explanatory notes to separate section
5. Consider adding prerequisite installation section for tools
