# Module 4 Fix: ReDoS (Regular Expression Denial of Service)

## Root Cause
CPU profiler revealed nearly all CPU time spent in regex engine during URL validation. The regex pattern has nested quantifiers that cause catastrophic backtracking on specific inputs (URLs with repeating characters).

**The mechanism**: Regex tries one path, fails, backtracks, tries another, fails, backtracks - potentially billions of combinations for a single input string. Like a maze where every dead end opens two more paths to explore.

**Problematic pattern example**: `/^https?:\/\/([\w.-]+)+(\/[\w.-])*$/` - nested `+` and `*` quantifiers create exponential backtracking on crafted inputs like `http://example.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!`

## Fix Options (in order of preference)

### Option 1: Replace regex with URL parser (BEST)
Use built-in URL parser instead of regex for validation:
```python
# Python
from urllib.parse import urlparse

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
```

```javascript
// Node.js
function validateUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}
```

**Advantages**: No regex, no backtracking, safer, standard library solution.

### Option 2: Rewrite regex to avoid backtracking
Use atomic groups or possessive quantifiers if regex engine supports them:
```python
# Python regex with atomic group (if using regex module)
import regex  # third-party, supports atomic groups
pattern = regex.compile(r'^https?://(?>([\w.-]+)+)(?>(/[\w.-])*)*$')
```

Or restructure pattern to eliminate nested quantifiers.

### Option 3: Add input length limit (DEFENSE IN DEPTH)
Reject URLs longer than 2048 characters before regex:
```python
MAX_URL_LENGTH = 2048

def validate_url(url):
    if len(url) > MAX_URL_LENGTH:
        return False
    # then apply regex validation
    return bool(url_pattern.match(url))
```

**Note**: This doesn't fix the regex but limits damage.

## Recommended Fix
Combine Option 1 and Option 3:
```python
from urllib.parse import urlparse

MAX_URL_LENGTH = 2048

def validate_url(url):
    if len(url) > MAX_URL_LENGTH:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
```

## Verification

**Test with malicious URL**:
```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"long_url": "http://example.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!"}'
```

**Expected result**:
- Response in milliseconds (not minutes)
- Either successful shortening or validation error
- CPU stays normal during request
- No 100% CPU spike on single core

**Profiler verification**: After fix, CPU profiler should show even distribution across functions, not regex validation dominating.

## Key Lessons

1. **ReDoS is real**: Regex with nested quantifiers can cause exponential backtracking
2. **CPU profiler reveals the truth**: Code reading wouldn't show the performance characteristics
3. **Standard library over regex**: Built-in URL parsers are safer than custom regex
4. **Defense in depth**: Input length limits as additional protection
5. **Malicious inputs matter**: Normal inputs work fine, crafted inputs expose vulnerabilities
