# Module 7 Reflection: Runbooks and Documentation

## Comprehension Questions

### 1. What core problem does this module solve in runbooks and documentation?
The module solves the problem of on-call engineers at 3 AM being cognitively impaired - equivalent to being legally drunk in every US state. Runbooks must be simple and linear, not decision trees, because stressed, sleep-deprived engineers cannot make good decisions. The core problem is that complex runbooks fail under stress - you need step-by-step instructions that can be followed without thinking.

### 2. Which decision in this module has the biggest impact, and why?
The runbook style decision (simple linear vs decision-tree) has the biggest impact. Simple linear runbooks have no branching or decisions - start at top, work down. Works for anyone regardless of experience level. Decision-tree runbooks require judgment and thinking, which fails when the engineer is sleep-deprived and stressed. A new team member on their first on-call shift can follow a linear runbook but cannot navigate a decision tree at 3 AM.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Runbook created with exact copy-paste commands for database down, cache failure, API timeout scenarios. Commands tested and verified to work. Each step has expected output. Escalation criteria added (10 minutes to senior engineer, page SRE for critical). Runbook is simple linear format - no decisions to make, just follow steps. Runbook can be followed by someone with no prior knowledge of the system.

## Mini Practical Task

### STEP 4 Verification: Runbook Commands

**Task**: Verify runbook commands work when copy-pasted

**Commands**:
```bash
# Database connectivity check
docker exec postgres pg_isready
# Expected output: postgres: ready

# Service health check
curl http://localhost:3000/health
# Expected output: {"status":"ok","database":"up","cache":"up"}

# View recent logs
docker logs notification-service --tail 50
# Expected output: Recent log lines visible
```

**Proof**: All commands execute successfully and return expected output. Commands are copy-pasteable and work without modification. Runbook can be followed by someone unfamiliar with the system.

## Risk and Mitigation

### Risk
**Missing escalation criteria**: Runbook doesn't specify when to escalate from self-resolution to paging senior engineers or SRE team. Engineer spends 2 hours trying to fix a database issue that requires database admin access, delaying resolution and causing extended outage.

### Mitigation
**Explicit escalation thresholds**: Add time-based escalation criteria - escalate to senior engineer after 10 minutes of troubleshooting, page SRE team immediately for critical service down or data loss. Specify what escalation means (Slack message, page, phone call) and who to contact (on-call database admin, SRE lead). Remove ambiguity about when to ask for help.

## Key Takeaways

1. **3 AM cognitive impairment**: On-call engineer at 3 AM is equivalent to being legally drunk - cannot make complex decisions or navigate branching logic.
2. **Linear runbooks**: Simple step-by-step instructions with no decisions. Start at top, work down. Works for anyone regardless of experience.
3. **Copy-paste commands**: Every command in runbook must be exact and copy-pasteable. No "check the logs" without specifying which log file and what to look for.
4. **Expected outputs**: Each step should show expected output so engineer knows if step succeeded or failed.
5. **Escalation criteria**: Explicit thresholds for when to escalate. Remove ambiguity about when to ask for help.
