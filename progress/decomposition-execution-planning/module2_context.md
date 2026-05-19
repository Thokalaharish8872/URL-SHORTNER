# Module 2 Context: Dependency Mapping

## Micro-Exercise: Draw a Simple DAG

**DAG Structure:**

```
    [A: Database Setup]
         /      \
        /        \
[B: User API]   [C: Provider Page]
        \        /
         \      /
      [D: Booking System]
```

**Answers:**

1. **Which tasks can happen at the same time?**
   Tasks B and C can happen in parallel (both need A but not each other).

2. **What is the longest chain from start to finish?**
   The longest chain is A -> B -> D (or A -> C -> D) - both are length 3 (critical path).

3. **If Task A takes twice as long as expected, which tasks are delayed?**
   Tasks B, C, and D are all delayed since they all depend on A directly or indirectly.
