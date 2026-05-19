def compute_dashboard_metrics(events):
    """Compute average, max, and throughput for analytics dashboard."""
    total_duration = sum(e["duration_ms"] for e in events)
    count = len(events)

    avg_duration = total_duration / count
    max_duration = max(e["duration_ms"] for e in events)
    throughput = count / (events[-1]["timestamp"] - events[0]["timestamp"])

    return {
        "avg_duration_ms": avg_duration,
        "max_duration_ms": max_duration,
        "throughput_per_sec": throughput,
    }
