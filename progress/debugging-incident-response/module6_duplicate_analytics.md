# Module 6 Break: Duplicate Analytics Bug

## Symptom
After deploying cache invalidation fix for Bug #9, analytics team reports duplicate analytics events. Every time a link is deleted and re-created with the same short code, the analytics job processes twice. Click counts are doubling for re-created links.

## Context
- Problem only affects links that are deleted and re-created
- Problem manifests as duplicate analytics processing
- Problem started after cache invalidation fix deployment
- Analytics processing handled by queue worker
- Fix added: `cache.del()` call to delete handler to invalidate redirect cache

## Hypothesis

### Hypothesis 1: Queue Worker Cache Dependency
The queue worker might be using the redirect cache as a signal or state for analytics processing. When we delete the cache entry on link deletion, the queue worker might:
- Lose track of whether it has already processed analytics for that link
- Re-process analytics when the link is re-created because cache is empty (looks like new link)
- Have a race condition where both the old and new analytics events get processed

### Hypothesis 2: Analytics Event Duplication
The analytics job might be triggered twice:
- Once when the original link is accessed before deletion (analytics event queued)
- Once when the re-created link is accessed (new analytics event queued)
- The queue worker might not be deduplicating events based on link_id, so both get processed

### Hypothesis 3: Cache Invalidation Side Effect
The `cache.del()` call might be deleting more than just the redirect cache key. If the cache key naming scheme overlaps with analytics cache keys (e.g., `link:{code}` for redirect and `link:{code}:analytics` for analytics), deleting one might accidentally delete the other, causing re-processing.

## Investigation Plan
1. Check what cache keys the queue worker reads or writes
2. Check if queue worker uses cache for deduplication or state
3. Check cache key naming scheme to identify potential overlap
4. Add logging to queue worker to see when analytics events are being processed
5. Reproduce by: create link, access it (generates analytics), delete link, re-create with same code, access again
