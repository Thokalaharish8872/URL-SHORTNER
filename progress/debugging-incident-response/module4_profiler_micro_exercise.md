# Module 4 Micro-Exercise: Profiling Tools

## Concepts

**Profiler**: A tool that observes the running system and tells you what's actually happening, not what the code says should happen. Like a GPS tracker for your code.

**CPU Profiler**: Tracks where processing time is spent. Answers: "Which function is my program stuck in?" Use when service is slow or pegging CPU.

**Memory Profiler**: Tracks where memory is allocated and whether it gets released. Answers: "Where is all the memory going?" Use when service grows larger over time or crashes with out-of-memory errors.

**Memory Leak**: Program allocates memory but never gives it back. Like a restaurant that seats guests but never clears tables - eventually cannot seat anyone.

**N+1 Query**: Code makes one query to get a list, then one additional query for each item. Turns one database round trip into fifty-one. Works correctly but catastrophically slow.

## Micro-Exercise Answers

### Question 1: Two tools or actions before reading code for 3-second API response

**Tool 1: CPU Profiler**
- Run a CPU profiler to see which function is consuming the most time
- Identifies bottlenecks like slow database queries, inefficient loops, or blocking operations
- Examples: cProfile for Python, pprof for Go, flame graphs

**Tool 2: Database Query Analysis**
- Check database query logs or use EXPLAIN ANALYZE on slow queries
- Identifies N+1 query patterns, missing indexes, or inefficient joins
- Examples: PostgreSQL slow query log, MongoDB profiler, AWS RDS Performance Insights

**Alternative actions**:
- Check application metrics (CPU, memory, I/O) to identify resource constraints
- Review recent deployments for correlation with performance degradation
- Test endpoint with curl to measure actual response time vs SLA

### Question 2: CPU profiler vs memory profiler for service getting slower over hours

**Difference**:
- CPU profiler: Shows where processing time is spent (which functions are slow)
- Memory profiler: Shows where memory is allocated and whether it's released (memory leaks)

**Which to pick for service getting slower over hours**: Memory profiler

**Reasoning**: "Gradually getting slower over hours" is a classic memory leak symptom. As memory leaks accumulate, the system spends more time in garbage collection, swapping to disk, or becomes resource-constrained. A CPU profiler would show the system spending time in GC or paging, but a memory profiler would show the root cause - memory that's allocated but never released.

The example from the module: Database connections created on every request but never closed on error path. After 2,000 requests, the pool was exhausted. A memory profiler would show this immediately; a CPU profiler would only show the symptom (slow responses).

## Key Takeaways

1. **Observe the running system**: When performance is the problem, profilers show what's actually happening, not what code says should happen
2. **CPU vs memory profilers**: Different dimensions - CPU shows time, memory shows allocation. Use the right tool for the symptom
3. **Memory leaks are insidious**: They work correctly until they don't - gradual degradation over time
4. **N+1 queries are silent performance killers**: They return correct data but are catastrophically slow
5. **Profile before reading code**: Tools reveal the actual bottleneck faster than code review
