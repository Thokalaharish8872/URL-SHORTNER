# Module 1 Bug #2: Pagination Is Broken

## Symptom
When users paginate through their list of short links, duplicate items appear across page boundaries. The last item on page 1 also appears as the first item on page 2.

## Hypotheses

### Hypothesis 1: OFFSET calculation is wrong
**Explanation**: Pagination works by skipping a certain number of records for each page. If the math is off by one, overlapping results occur.
- Expected: Page 1 shows records 1-10, page 2 shows records 11-20
- Actual: Page 1 shows records 1-10, page 2 shows records 10-19 (overlap)

**Test**: Inspect the actual SQL query being generated for page 1 and page 2. Check the OFFSET and LIMIT values.
- Command: Enable query logging or add print statements to see the generated SQL
- Expected: Page 1: OFFSET 0 LIMIT 10, Page 2: OFFSET 10 LIMIT 10
- If overlapping: OFFSET values are incorrect

### Hypothesis 2: Sort order is unstable
**Explanation**: If the database doesn't return results in a consistent order, the same record could appear in different positions on different queries.

**Test**: Run the same query twice in quick succession and compare results.
- Command: Run page 1 query and page 2 query back-to-back
- Check: Do records overlap between the two queries?
- If order is unstable: Same record appears in different positions

## Investigation

### Check existing implementation
Looking at `api/app/services.py` line 237-241:
```python
@staticmethod
def list_links(db: Session, creator: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Link]:
    query = select(Link)
    if creator:
        query = query.where(Link.created_by == creator)
    return list(db.execute(query.offset(skip).limit(limit)).scalars().all())
```

### Analysis
The implementation uses `offset(skip)` and `limit(limit)` which is correct SQLAlchemy syntax.
- Page 1: skip=0, limit=10 → records 0-9 (first 10)
- Page 2: skip=10, limit=10 → records 10-19 (next 10)
- Page 3: skip=20, limit=10 → records 20-29 (next 10)

This implementation appears correct. The off-by-one error must be in how the `skip` parameter is calculated from the page number.

### Common Off-by-One Error Pattern
If the calculation is:
- skip = (page - 1) * limit ✓ Correct
- skip = page * limit ✗ Wrong (causes overlap)

### Fix
Ensure the skip calculation is:
```python
skip = (page - 1) * limit
```

### Verification
Test with curl across three pages:
```bash
curl -sS "http://localhost:8000/links?skip=0&limit=10"   # Page 1
curl -sS "http://localhost:8000/links?skip=10&limit=10"  # Page 2
curl -sS "http://localhost:8000/links?skip=20&limit=10"  # Page 3
```

Check that:
- Every item appears on exactly one page
- No items are duplicated across page boundaries
- Total unique items = (items on page 1) + (items on page 2) + (items on page 3)

## Key Lesson
Off-by-one errors are among the most common bugs. They occur when a calculation is wrong by exactly one (using `page * limit` instead of `(page - 1) * limit`). These are easy to miss in code review because the logic looks almost right.

Hypothesis-first debugging helps catch these quickly by testing the simpler hypothesis (check the math) before diving into complex code inspection.
