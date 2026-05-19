# Module 4 Performance Bugs: Memory Leak and N+1 Query

## Bug #6: Memory Leak - Database Connections Not Released

### Symptom
Service gradually gets slower over hours, eventually crashes or becomes unresponsive. Response times creep up: 100ms → 300ms → 800ms → timeouts.

### Investigation
**Tool**: Memory profiler (heap profiler)

**Finding**: Database connections created on every request but never closed on the error path. Happy path releases connections properly, but the 2% of requests that hit errors leak them. After 2,000 requests, the pool is exhausted.

**Root cause**: Connection release logic only in success path, not in finally block. When errors occur, connections remain allocated.

### Fix
Move connection release to finally block - code that runs whether operation succeeds or fails:
```python
try:
    connection = pool.acquire()
    result = connection.query(...)
    return result
catch error:
    log(error)
    return error_response
finally:
    if connection:
        connection.release()  # runs no matter what
```

### Verification
Run 2,000 requests, monitor memory throughout. Should stay flat (minor GC fluctuations fine, no upward trend). Connection object count should stay constant (equal to pool size), not grow with request count.

**Key lesson**: Code looked correct if you only read happy path. Profiler showed real execution path - the one where errors happen.

## Bug #7: N+1 Query on Links Endpoint

### Symptom
GET /links endpoint takes over 3 seconds with just 50 rows. Code hasn't changed recently. Used to be fast, now not.

### Investigation
**Tool**: Query logging (database-side or ORM-side)

**Enable query logging**:
- PostgreSQL: Set `log_min_duration_statement = 0`
- SQLAlchemy: Set `echo=True` on engine
- Sequelize/TypeORM: Enable logging in connection options

**Finding**: 51 queries for single request
```sql
SELECT * FROM links ORDER BY created_at DESC LIMIT 50;  -- 1 query
SELECT * FROM analytics WHERE link_id = 1;          -- N queries (50)
SELECT * FROM analytics WHERE link_id = 2;
...
SELECT * FROM analytics WHERE link_id = 50;
```

**Root cause**: N+1 pattern - 1 query for list, N queries for related data. ORM configuration specified eager loading, but recent dependency update changed default behavior. Config still says "eager" but ORM silently ignores it because syntax/option name changed between versions.

**Category**: Bug code reading almost never catches - code looks right, config looks right, but runtime behavior changed due to dependency update.

### Fix
Explicitly configure eager loading in way current ORM version respects:

**SQLAlchemy**:
```python
links = db.session.query(Link).options(
    joinedload(Link.analytics)
).order_by(Link.created_at.desc()).limit(50).all()
```

**Raw JOIN query** (if ORM fighting you):
```sql
SELECT links.*, analytics.click_count
FROM links
LEFT JOIN analytics ON analytics.link_id = links.id
ORDER BY links.created_at DESC
LIMIT 50;
```

### Verification
1. Hit GET /links with query logging enabled - should see 1-2 queries, not 51
2. Measure response time - should be under 200ms with 50 rows
3. Run EXPLAIN ANALYZE on JOIN query to confirm it uses indexes

## Key Lessons

1. **Profilers show actual behavior**: Code tells you what should happen, profiler tells you what does happen
2. **Memory leaks are insidious**: They work correctly until they don't - gradual degradation
3. **Query logging reveals N+1**: Enable SQL logging to see actual queries ORM generates
4. **Dependency updates can break silently**: Config looks right but runtime behavior changes
5. **Finally blocks for cleanup**: Always use finally blocks for resource cleanup, not just success path
