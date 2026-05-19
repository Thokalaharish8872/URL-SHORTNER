# Module 7 Micro-Exercise: Blameless Postmortem

## Postmortem Definition
A postmortem (post-incident review) is a structured document written after an incident that answers three questions:
1. What happened?
2. Why did the system allow it to happen?
3. What do we change so this class of failure cannot happen again?

The third question is the one that matters - not "what do we change so this exact bug never recurs" (that's a patch), but "what do we change so this CLASS of failure cannot happen again" (that's engineering).

## Blameless Does Not Mean Unaccountable

**Blameless**: We do not point fingers at individuals. We do not name the person who wrote the bug or approved the pull request. Not because those people did nothing wrong, but because blaming them doesn't fix anything and actively makes the next incident worse.

**Analogy**: When an airplane crashes, the NTSB doesn't jail the pilot. They ask: what about cockpit design allowed this mistake? What about the procedure created ambiguity? Then they redesign the cockpit and rewrite the procedure. The next pilot is safer because the system around them is better.

**Accountability**: Blameless doesn't mean nobody is accountable. It means we recognize humans make mistakes (that's a fact, not a flaw) and systems should catch mistakes before they reach production. If one person's typo can take down production, the problem is not the person - it's the system that let a typo reach production unchecked.

**Culture impact**: When postmortems are not blameless, people hide mistakes, cover tracks, avoid touching risky code. Bugs still exist but people stop talking about them. Google's SRE team attributes their reliability to postmortem culture - when people are safe to report mistakes, mistakes get reported early before they compound.

## Micro-Exercise: Blameless Language Transformation

### Original (Blame-full)
"The junior developer pushed untested code to production, causing the outage."

### Blameless Rewrite
"A code change was deployed to production without passing through the test suite. The deployment pipeline did not enforce test passage as a merge requirement."

**What changed**: The person disappeared. The action is still there (code deployed without tests) but the focus shifted from WHO did it to WHAT SYSTEM ALLOWED it. The first version implies "hire better developers." The second version implies "fix the pipeline." Only one prevents the next incident.

### Additional Examples

**Blame-full**: "The engineer forgot to set the environment variable."
**Blameless**: "The application did not validate that required environment variables were set at startup."

**Blame-full**: "The ops team didn't monitor the connection pool."
**Blameless**: "The monitoring system did not alert when connection pool utilization exceeded threshold."

**Blame-full**: "The tester missed the edge case."
**Blameless**: "The test suite did not include coverage for the edge case scenario."

## Key Principle

**Subject should be the system, not a human**: The pipeline, the process, the deployment system, the validation logic - not the developer, the engineer, the ops team, the tester. If your rewrite still has a person as the subject ("The developer should have..."), try again.
