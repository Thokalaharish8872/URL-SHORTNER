# Flawed Design Document Analysis

## Gap 1: Missing "Alternatives Considered" Section

**What's missing:** The document has no "Alternatives Considered" section at all.

**Why this is dangerous:** Without alternatives, reviewers can't tell if the author genuinely evaluated other options or just picked Apache Kafka because it's popular. Maybe a message queue like RabbitMQ would be sufficient for 2,000 events/second. Maybe cloud-native options like AWS Kinesis or Google Pub/Sub would be cheaper and require less infrastructure. The team could build the wrong architecture for their needs because they never considered alternatives.

**Impact:** Months of engineering work on a solution that might be overkill or misaligned with actual requirements.

---

## Gap 2: Critical Assumption Stated as Fact

**The claim:** "The publish operation takes <5ms, compared to the current 150-300ms of synchronous processing."

**Why this is dangerous:** This is stated as fact but has never been validated. If the actual publish time is 50ms or 100ms (due to network latency, serialization, authentication, etc.), the entire latency benefit calculation falls apart. The business case for this project is built on reducing API latency from 150-300ms to <5ms. If that's wrong, the project shouldn't be done at all.

**Second critical assumption:** "The analytics database benchmarks show capacity for 10,000 writes/second, so we have plenty of headroom." Benchmarks are not production. Real-world workloads have different patterns, contention, and failure modes that benchmarks don't capture.

**Impact:** Project proceeds based on false premises, fails to deliver promised benefits, and the team wastes 7 weeks.

---

## Gap 3: Vague Risk Mitigations

**The mitigation:** "we will monitor consumer lag closely and scale up consumers if needed"

**Why this is dangerous:** At 3 AM, what does "closely" mean? What lag threshold triggers an alert? What lag threshold requires scaling? How do you scale consumers manually? Is there an auto-scaling policy? How long does it take to spin up new consumers? This mitigation is too vague to act on in an emergency.

**Second vague mitigation:** "we will configure replication factor of 3 across brokers" for Kafka cluster failure. This provides redundancy but doesn't prevent data loss if the entire cluster goes down. There's no mention of what happens when events are published during an outage - do they get buffered? Lost? Retried?

**Impact:** When risks materialize (which they will), the on-call engineer can't actually execute the mitigation because it's not specific enough. They're flying blind.
