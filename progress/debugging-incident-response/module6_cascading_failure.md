# Module 6 Cascading Failure: Connection Pool Exhaustion

## Symptom
API becomes unresponsive, health checks time out, monitoring reports API as down. But individual components (cache, database, queue) all appear healthy in isolation.

## Investigation Strategy
Chose vertical investigation - following a single request through the entire stack to reveal handoff issues between layers, since each layer's health check passes but the system is broken.

## Root Cause Analysis

### Chain of Causation
1. A queue job fails (bad data, temporary DB hiccup, anything)
2. Queue worker retries immediately (no backoff)
3. Each retry acquires a DB connection from the shared pool
4. The retry fails again (same error)
5. Worker retries again immediately (no max retry count)
6. Steps 3-5 repeat in a tight loop
7. Shared connection pool is exhausted within seconds
8. API requests that need the database cannot get a connection
9. API requests hang indefinitely, waiting for connections
10. Entire API becomes unresponsive
11. Health checks (which also need the database) time out
12. Monitoring reports the API as down

**Symptom at step 12, root cause at step 1**

### Design Flaws
- Step 2: No backoff delay - retries happen immediately
- Step 5: No maximum retry count - retries continue forever
- Step 7: Shared connection pool - queue workers and API share the same pool

## Fix (All Three Required)

### 1. Add Exponential Backoff
Instead of retrying immediately, wait 1 second, then 2, then 4, then 8, etc. This prevents the tight loop that burns through connections.

```python
# Celery configuration
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_SOFT_TIME_LIMIT = 300

# Retry with exponential backoff
@app.task(bind=True, max_retries=5)
def process_click_event(self, event_data):
    try:
        # Process the event
        pass
    except Exception as exc:
        # Exponential backoff: 2^retry_count seconds
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

### 2. Set Maximum Retry Count
After 5 retries, mark the job as permanently failed and move it to a dead-letter queue for manual inspection.

```python
@app.task(bind=True, max_retries=5)
def process_click_event(self, event_data):
    try:
        # Process the event
        pass
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            # Move to dead-letter queue
            dead_letter_queue.send(event_data)
            return
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

### 3. Use Separate Connection Pool
Queue workers and API should not share the same connection pool. Give queue workers their own smaller pool (e.g., 3 connections out of 20 total). This is resource isolation - like bulkheads on a ship.

```python
# API connection pool
api_engine = create_engine(
    DATABASE_URL,
    pool_size=17,  # 17 for API
    max_overflow=0
)

# Worker connection pool
worker_engine = create_engine(
    DATABASE_URL,
    pool_size=3,  # 3 for workers
    max_overflow=0
)
```

## Verification
1. Trigger a queue job failure deliberately
2. Watch retry behavior - should back off exponentially
3. After max retries, job should land in dead-letter queue
4. Throughout the entire process, make API requests - should respond normally
5. API should never become unresponsive due to queue worker behavior

## Key Lessons

1. **Cascading failures are invisible**: Problem in one component (queue worker) chokes a completely different component (API) through shared resources
2. **Health checks test isolation**: Each component looks healthy alone, but the interaction breaks the system
3. **Resource isolation is critical**: Shared connection pools create hidden coupling points
4. **Retry policies matter**: No backoff + no max retry = infinite loop that exhausts resources
5. **Vertical investigation reveals interactions**: Following a single request through the stack shows handoff failures that horizontal checks miss
