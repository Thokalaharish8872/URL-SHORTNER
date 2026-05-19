## Design Document: Event Processing Pipeline (Fixed)

Author: Jamie Chen
Date: March 15, 2025
Status: Proposed

### Problem Statement

Our application generates user activity events (page views, clicks, purchases) that we currently process synchronously during the API request. This adds 150-300ms of latency to every request. As traffic grows, this synchronous processing will become a bottleneck. We need to move event processing out of the request path to keep API response times fast.

### Proposed Approach

We will implement an asynchronous event processing pipeline using Apache Kafka.

Events will be published to Kafka topics during the API request. The publish operation takes <5ms, compared to the current 150-300ms of synchronous processing. Separate consumer services will read events from Kafka and process them independently.

Architecture:

1. API servers publish events to Kafka topics (one topic per event type)
2. Consumer services subscribe to topics and process events
3. Processed results are written to the analytics database
4. Failed events are retried up to 3 times, then sent to a dead letter queue for manual inspection

Implementation plan:
- Week 1-2: Set up Kafka cluster (3 brokers) and create topics
- Week 3-4: Modify API to publish events asynchronously
- Week 5-6: Build consumer services for each event type
- Week 7: Integration testing and cutover

### Alternatives Considered

**Alternative 1: In-process background queue (Sidekiq)**
- What it is: A background job queue running on each application server using local memory
- Why someone might choose it: No new infrastructure to deploy, simpler to operate, no external dependencies
- Why not recommending: Limited to single server memory (no cross-server coordination), no persistence if server crashes, doesn't scale horizontally beyond the number of API servers

**Alternative 2: Managed queue service (AWS SQS)**
- What it is: Fully managed message queue service provided by AWS
- Why someone might choose it: No infrastructure to manage, built-in retry and dead letter queues, pay-per-use pricing
- Why not recommending: Adds cloud vendor dependency, per-message costs at scale (2,000 events/second = expensive), less control over configuration and performance tuning

### Risks

**Risk 1: Kafka cluster failure**
- Mitigation: Configure replication factor of 3 across brokers. Set up Datadog alert on broker health. If any broker goes down, auto-replacement script triggers within 5 minutes. If majority of brokers fail, failover to backup cluster in secondary region.

**Risk 2: Consumer lag**
- Mitigation: Set Datadog alert on consumer lag exceeding 10,000 messages. If alert fires, on-call engineer runs `./scale-consumers.sh` to add instances (documented in runbook). If lag does not recover within 15 minutes, escalate to platform team lead.

**Risk 3: Data consistency**
- Mitigation: For order-sensitive events (like purchases), use a single partition to guarantee ordering. Add sequence numbers to events for client-side reordering if needed.

**Risk 4: Doing nothing**
- Impact: API latency continues to increase as traffic grows, manual intervention for performance issues becomes more frequent, product team cannot launch features requiring real-time event processing.

### Open Questions

**Question 1: Can the analytics database sustain 10K writes/second under production conditions?**
The current benchmark showing 10K writes/second capacity was run under unknown conditions. Before implementation begins, the database team should run a load test simulating the actual event schema, indexing pattern, and concurrent read load. If the database cannot handle the projected write volume, we may need to add a write-ahead buffer or switch to a time-series database for event storage.

**Question 2: What is the actual publish latency to Kafka?**
The document assumes <5ms publish time, but this has not been validated. We need to measure actual publish latency including network overhead, serialization, and authentication before committing to this approach.

**Question 3: What are the specific rate limits for different event types?**
Do all events need real-time processing, or can some be batched? This affects topic design and consumer scaling strategy.

### Timeline

Seven weeks from approval to production cutover. Team of 3 engineers.
