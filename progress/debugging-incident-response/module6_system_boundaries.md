# Module 6 Micro-Exercise: System Boundaries

## Concepts

**Multi-layer bug**: Bug exists not in a single component but in the missing agreement between components. Like orchestra where each section is in tune but the whole performance is wrong because they're playing different songs.

**Connection pool exhaustion**: When all database connections in the pool are occupied and none are released. The pool "works" - it has spaces, gates are open - but every space is occupied. New requests wait for connections that never free up. API doesn't crash, just stops responding.

**Cascading failure**: One failure causes another in a chain reaction. Like freeway pile-up - one car stops, rear-end collisions travel backward. In software: problem in one component (queue worker retrying aggressively) creates resource pressure that chokes a different component (API).

## System Boundary Mapping

### Boundary 1: API → Cache
**Where**: API reads link data from Redis cache before querying database

**Assumption**: API assumes cache has current data or will return null if data doesn't exist
**Documentation**: Not documented
**Enforcement**: Not enforced - cache can have stale data if cache invalidation fails
**Risk**: Cache returns stale data, API serves outdated information to users

### Boundary 2: API → Database
**Where**: API queries PostgreSQL for link data, analytics, user information

**Assumption**: API assumes database is available and will return consistent data
**Documentation**: Partially documented in connection pool configuration
**Enforcement**: Partially enforced by connection pool limits and retry logic
**Risk**: Connection pool exhaustion causes API to hang waiting for connections

### Boundary 3: API → Celery Queue
**Where**: API enqueues click events to Celery for asynchronous processing

**Assumption**: API assumes queue accepts messages and workers will process them eventually
**Documentation**: Not documented
**Enforcement**: Not enforced - queue can be full or workers can be dead
**Risk**: Queue fills up, API blocks waiting for enqueue, or messages lost if queue crashes

### Boundary 4: Celery Workers → Database
**Where**: Celery workers query and update database for analytics aggregation

**Assumption**: Workers assume database connection pool is shared but not exhausted by API
**Documentation**: Not documented
**Enforcement**: Not enforced - workers and API share same connection pool
**Risk**: Workers exhaust connection pool, API cannot get database connections

### Boundary 5: Celery Workers → Redis
**Where**: Workers use Redis for task coordination and result storage

**Assumption**: Workers assume Redis is available for locking and state management
**Documentation**: Not documented
**Enforcement**: Partially enforced by retry logic
**Risk**: Redis failure causes workers to hang or duplicate task processing

## Key Insights

1. **Assumptions are invisible**: Most boundaries are based on assumptions that aren't documented or enforced
2. **Health checks test isolation**: Each component looks healthy in isolation, but the contracts between them break
3. **Shared resources create coupling**: Connection pool shared between API and workers is a hidden coupling point
4. **Cascading failures are invisible**: Problem in queue workers can choke API through shared resource pool
5. **Need boundary contracts**: Each boundary should have documented, enforced assumptions (timeouts, circuit breakers, rate limits)
