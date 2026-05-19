# Module 6 Reflection: Multi-Layer Bugs

## Comprehension Questions

### 1. What core problem does this module solve in multi-layer bugs?
The module solves the problem of debugging bugs that exist in the interaction between components rather than within individual components. Multi-layer bugs resist standard debugging approaches because each component's health check passes while the system is broken. The core skill is tracing causation across layers, identifying systemic design flaws (shared resources, missing boundary contracts), and understanding that the bug is in the missing agreement between components, not in any single component.

### 2. Which decision in this module has the biggest impact, and why?
The investigation strategy decision (vertical vs horizontal) has the biggest impact. Choosing vertical investigation - following a single request through the entire stack - reveals the exact handoff where things go wrong by watching interactions between layers. Horizontal investigation checks components in isolation, which is exactly the condition where multi-layer bugs don't appear. Given that each layer's health check passes but the system is broken, the bug is in the handoff between layers, which only a vertical trace can reveal.

### 3. What evidence proves the implementation works end-to-end?
For cascading failure fix: Trigger queue job failure deliberately - retry behavior shows exponential backoff, after max retries job lands in dead-letter queue. Throughout the process, API requests respond normally - API never becomes unresponsive due to queue worker behavior. For cache namespace fix: Delete link - confirms immediate 404 (Bug #9 fix still works). Re-create link with same short code - analytics job processes exactly once. Check Redis - shows two distinct keys with different prefixes (redirect:link:abc and dedup:link:abc).

## Mini Practical Task

### STEP 4 Verification: Multi-Layer Bugs

**Task**: Verify cache namespace separation prevents duplicate analytics

**Verification commands**:
```bash
# Create a link
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
# Response: {"short_code": "abc", ...}

# Access the link to generate analytics event
curl http://localhost:8000/abc
# Response: 301 redirect

# Delete the link
curl -X DELETE http://localhost:8000/links/abc
# Response: 204 No Content

# Verify 404 immediately
curl http://localhost:8000/abc
# Response: 404 Not Found

# Re-create link with same short code
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com", "custom_code": "abc"}'
# Response: {"short_code": "abc", ...}

# Access the re-created link
curl http://localhost:8000/abc
# Response: 301 redirect

# Check Redis keys
redis-cli KEYS "*link:abc*"
# Expected output:
# 1) "redirect:link:abc"
# 2) "dedup:link:abc"
# Should show TWO distinct keys with different prefixes

# Check analytics count
# Should be 2 (one from original link, one from re-created link)
# NOT 4 (which would indicate duplicate processing)
```

**Proof**: Redis shows two distinct keys with different prefixes (redirect:link:abc and dedup:link:abc), confirming namespace separation. Analytics count is 2 (correct), not 4 (which would indicate duplicate processing).

## Risk and Mitigation

### Risk
**Shared cache key namespaces**: Two different systems using the same key pattern for different purposes creates hidden coupling. A change to one system (adding cache invalidation) can break the other (deduplication) without any obvious connection.

### Mitigation
**Namespace separation with prefixes**: Use distinct key prefixes for different purposes (redirect:link:<id> vs dedup:link:<id>). Document and enforce boundary contracts between systems. This prevents interference and makes the coupling explicit rather than hidden.

## Key Takeaways

1. **Multi-layer bugs hide in interactions**: Components look healthy in isolation, but the contracts between them break
2. **Vertical investigation reveals handoffs**: Following a single request through the stack shows interaction failures
3. **Shared resources create hidden coupling**: Connection pools, cache keys, and queues are invisible coupling points
4. **Namespace separation prevents interference**: Distinct prefixes for different purposes prevent accidental cross-system effects
5. **Fixes can introduce new bugs**: The cache invalidation fix for Bug #9 created the duplicate analytics bug by affecting shared keys
