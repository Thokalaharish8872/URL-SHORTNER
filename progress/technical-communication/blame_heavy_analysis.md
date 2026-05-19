# Blame-Heavy Postmortem Analysis

## Blame Instances (19 found)

1. "John Chen deployed OrderProcessor v2.14, which contained a breaking configuration change" - names individual in negative context
2. "John removed the warehouse_routing config field without verifying" - names individual in negative context
3. "This should not have happened" - judgmental language
4. "John did not check whether the production service still read it at runtime" - names individual in negative context
5. "This was an oversight on John's part" - judgmental language
6. "Maria Santos, the on-call engineer, initially dismissed the customer reports" - names individual in negative context
7. "Maria should have investigated immediately" - judgmental language directed at individual
8. "Maria could have checked the database directly sooner" - judgmental language directed at individual
9. "DevOps had not updated it" - names team in negative context
10. "John removed a config field that the service still depended on" - names individual in root cause
11. "John should have verified backwards compatibility" - judgmental language directed at individual
12. "Maria did not investigate the initial customer reports quickly enough" - names individual in contributing factors
13. "Kevin's team had not maintained the rollback automation" - names individual in contributing factors
14. "John did not do a thorough enough review" - names individual in contributing factors
15. "John will be more careful" - action item directed at individual (be more careful trap)
16. "Maria should set up better monitoring" - action item directed at individual
17. "Kevin's team should fix the rollback script" - action item directed at team
18. "This outage was avoidable if John had done more thorough testing" - lessons learned blames individual
19. "Everyone should double-check their work" - universal blame

## Answers to Questions

**1. What systemic root cause did this postmortem completely miss?**
The postmortem completely misses the question: "why does removing a config field cause silent data loss instead of a loud failure?" The real systemic root causes are:
- Broad error handling that suppresses failures and returns 200 OK
- No config schema validation in deployment pipeline
- Monitoring that checks service health but not business health (order creation rate)
- Untested rollback automation

These systems made the config field removal dangerous, not the individual who removed it.

**2. How many of the five action items are actually system changes?**
Zero. All five action items are "be more careful" in different words:
1. "John will be more careful" - human behavior
2. "Remind the team to always check backwards compatibility" - human behavior
3. "Maria should set up better monitoring" - vague, no system change specified
4. "Kevin's team should fix the rollback script" - the only one that's a system change, but it's directed at a team/person rather than a process
5. "Add a review step where someone double-checks config changes" - this could be a system change, but it's framed as "someone double-checks" rather than an automated validation

**3. If you were John, Maria, or Kevin, would you report a near-miss next time?**
No. Knowing that my name will end up in a document circulated to the whole team, I would keep near-misses quiet. The blame-heavy culture incentivizes hiding mistakes rather than reporting them. This reduces visibility into system failures and makes the overall system less safe.

**4. What will this postmortem prevent?**
Nothing for the next engineer. If John is "more careful," maybe John won't make this exact mistake again. But the next engineer who removes a deprecated config field will face the same dangerous system - no config validation, silent error handling, no business health monitoring. The postmortem fixes nothing about the system that made this incident possible.
