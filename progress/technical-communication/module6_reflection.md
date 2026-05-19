# Module 6 Reflection: Documentation

## Comprehension Questions

1. **What core problem does this module solve in documentation that gets read?**
   This module solves the problem of documentation that becomes stale and fails when needed most. It teaches the importance of copy-pasteable commands, no assumed knowledge, scannable structure under pressure, and maintenance processes (verification schedules, update-on-change requirements) to keep operational documents accurate over time.

2. **Which decision in this module has the biggest impact, and why?**
   The documentation strategy decision (comprehensive vs minimal+links) has the biggest impact because it determines whether documentation stays current. Comprehensive docs in one place become stale quickly because nobody maintains them. Minimal+links keeps each tool current because people use it daily, but risks broken links and fragmented information. The decision affects whether documentation is accurate when needed at 3 AM.

3. **What evidence proves the implementation works end-to-end?**
   The fixed runbook (orderflow_runbook_fixed.md) demonstrates the implementation works: it includes maintenance metadata (last verified date, review cadence), all copy-pasteable commands with no placeholders, tool prerequisites section, numbered steps for each failure mode, and known failure modes table. It applies the 3 AM test - can someone follow it alone under pressure with no prior context.

## Mini Practical Task

**STEP 4 verification for orderflow_runbook_fixed.md:**

**Constants section excerpt:**
"**Service Name:** orderflow
**Namespace:** production
**API Port:** 8080
**On-call Slack:** #orderflow-oncall"

**Change made:** Added constants section at top of runbook to eliminate duplication. Previously, values like port 8080, namespace "production", and Slack channels were hardcoded in multiple places. Defining them once at the top means when values change, one edit fixes the whole document. This prevents the GitLab situation where the backup tool changed but the runbook wasn't updated.
