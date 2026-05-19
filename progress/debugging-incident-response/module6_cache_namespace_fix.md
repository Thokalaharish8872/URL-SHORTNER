# Module 6 Fix: Cache Key Namespace Separation

## Root Cause
The redirect cache and deduplication cache were using the same key pattern `link:<id>` for two different purposes:
- Redirect cache: stores target URL for fast redirects
- Deduplication flag: marks analytics jobs as processed

When Bug #9 fix added `cache.del(link:<id>)` on link deletion, it cleared both the redirect cache (correct) AND the deduplication flag (unintended side effect).

## Sequence of Failure
1. Link exists - redirect cache has `link:abc` with target URL, queue worker processed analytics job and saw `link:abc` exists (knows it already ran)
2. Delete link - new cache invalidation runs `DEL link:abc` - clears redirect cache (correct) but also clears deduplication flag (unintended)
3. Re-create link with same short code - new analytics job enters queue
4. Queue worker checks `link:abc` - key doesn't exist (deleted in step 2)
5. Worker concludes it has NOT processed this job yet - processes analytics job again
6. Duplicate event

## Fix: Separate Cache Key Namespaces

Use distinct prefixes for different purposes:
- Redirect cache: `redirect:link:<id>` - stores the target URL for fast redirects
- Deduplication flag: `dedup:link:<id>` - marks analytics jobs as processed

### Code Changes

**Redirect handler update**:
```python
# Before
cache_key = f"link:{link_id}"
target_url = cache.get(cache_key)

# After
cache_key = f"redirect:link:{link_id}"
target_url = cache.get(cache_key)
```

**Delete handler update**:
```python
# Before
cache_key = f"link:{link_id}"
cache.del(cache_key)

# After
cache_key = f"redirect:link:{link_id}"
cache.del(cache_key)
```

**Queue worker update**:
```python
# Before
dedup_key = f"link:{link_id}"
if cache.exists(dedup_key):
    return  # already processed
cache.set(dedup_key, "1", ttl=86400)  # 24 hours

# After
dedup_key = f"dedup:link:{link_id}"
if cache.exists(dedup_key):
    return  # already processed
cache.set(dedup_key, "1", ttl=86400)  # 24 hours
```

## Verification
1. Delete a link - confirm it immediately returns 404 (Bug #9 fix still works)
2. Re-create link with same short code - confirm analytics job processes exactly once (not zero, not two)
3. Check Redis - should see two distinct keys with different prefixes:
   - `redirect:link:abc` - for redirect cache
   - `dedup:link:abc` - for deduplication flag

## Key Lesson

**Shared keys create hidden coupling**: Two different systems (redirect handler and queue worker) were using the same cache key pattern without documentation or enforcement. This created a hidden boundary where a change to one system (adding cache invalidation) broke the other (deduplication). The fix is namespace separation - each system should have its own key space to prevent interference.

This is a multi-layer bug where the issue was in the missing agreement between components, not within any single component.
