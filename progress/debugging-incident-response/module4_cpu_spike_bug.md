# Module 4 Break: CPU Spike on Specific URLs

## Symptom
After deploying fixes for memory leak and N+1 query, a new issue emerged:
- Single POST /links requests taking 47-52 seconds, timing out at 60 seconds
- Most requests fine (<100ms)
- Only requests with specific URLs affected
- URLs with unusually long repeating characters: `http://example.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!`
- CPU spikes to 100% on single core for duration of affected request
- No errors in logs
- Database is fast
- Memory is stable

## Investigation Approach
**Tool**: CPU profiler (not code reading first)

## Hypothesis Formation

### Hypothesis 1: Repeated Character Processing
URLs with repeating characters might trigger an algorithm with O(n²) or exponential time complexity. Common culprits:
- Regex without backtracking limits
- String comparison algorithms on repeated patterns
- Validation functions that don't handle edge cases

### Hypothesis 2: Custom Code Generation
The short code generation function might use an algorithm that degrades with certain input patterns (like repeated characters in the original URL).

### Hypothesis 3: Encoding/Decoding Operations
URL encoding/decoding or base64 operations might have pathological cases with specific character patterns.

## Profiling Investigation

**Step 1: Reproduce the issue**
```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"long_url": "http://example.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!"}'
```

**Step 2: Attach CPU profiler**
```bash
# Python
py-spy top --pid <process_id>

# Or with sampling profile
py-spy record -o profile.svg --pid <process_id>
```

**Expected finding**: CPU profiler will show 100% time spent in a specific function, likely related to string processing or custom code generation.

## Likely Root Cause

Based on the pattern (repeating characters cause CPU spike), this is likely a **ReDoS (Regular Expression Denial of Service)** or similar algorithmic complexity issue.

**Common pattern**: A regex like `^a+$` on a string of 10,000 'a' characters can cause catastrophic backtracking if the regex engine tries multiple match positions.

**Alternative**: Custom code generation algorithm that tries to derive a short code from the URL hash and has poor performance on certain hash patterns (which correlate with repeating characters in the input).

## Fix Strategy

1. **For regex issues**: Add timeouts to regex operations, use non-backtracking engines, or rewrite regexes to be linear-time
2. **For algorithmic issues**: Add input validation (max URL length), use O(n) algorithms instead of O(n²), or add timeouts to processing
3. **For code generation**: Cache results, limit iterations, or use a different algorithm

## Verification

After fix, test with the problematic URL:
- Response time should be <100ms
- CPU should not spike to 100%
- Profiler should show even distribution across functions, not one function dominating

## Key Insight

CPU profiler is essential here - code reading would not reveal the performance characteristics. The code might look correct (standard regex, standard algorithm), but runtime behavior on specific inputs reveals the pathological case. Only by observing the running system can you see which function is consuming CPU.
