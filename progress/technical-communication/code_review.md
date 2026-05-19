# Code Review: `compute_dashboard_metrics`

## Summary

The function needs hardening before it can safely power the analytics dashboard. **There is a critical division-by-zero risk when `events` is empty**, and two additional edge cases that will crash the dashboard or return misleading data.

---

## Priority Issues

### 🔴 Critical: Division-by-zero on empty `events`
**Line 6:** `avg_duration = total_duration / count`

If `events` is an empty list, `count` is `0` and the function raises `ZeroDivisionError`. The dashboard will 500 instead of gracefully showing "no data."

**Suggested fix:**
```python
if count == 0:
    return {"avg_duration_ms": 0, "max_duration_ms": 0, "throughput_per_sec": 0}
```

### 🟠 High: `max()` on empty iterable
**Line 7:** `max_duration = max(e["duration_ms"] for e in events)`

`max()` raises `ValueError` on an empty sequence. This is a second crash path even if the division-by-zero were patched independently.

**Suggested fix:** Guard with `if events:` or provide a default.

### 🟡 Medium: Throughput timestamp assumption
**Line 8:** `throughput = count / (events[-1]["timestamp"] - events[0]["timestamp"])`

- Assumes `events` is chronologically sorted. If the caller passes unsorted data, throughput is wrong.
- If all events share the same timestamp, another division-by-zero occurs.
- If `events` has only one element, the denominator is `0`.

**Suggested fix:**
```python
sorted_events = sorted(events, key=lambda e: e["timestamp"])
time_span = sorted_events[-1]["timestamp"] - sorted_events[0]["timestamp"]
throughput = count / time_span if time_span > 0 else 0
```

---

## Questions for the Author

1. Should the function accept an iterator, or is a list guaranteed? If an iterator, `len()` and indexing will fail.
2. What is the expected unit for throughput? "per_sec" suggests seconds, but the timestamps appear to be raw epoch integers — should we divide by 1000?
3. Do we need to handle single-event edge cases in the dashboard, or should the caller filter them out?

---

## Positive Notes

- The return shape is clean and consistent, which makes frontend binding straightforward.
- Using a dict literal keeps the code readable.

---

**Verdict:** Request changes — the empty-input crash paths must be resolved before merge.
