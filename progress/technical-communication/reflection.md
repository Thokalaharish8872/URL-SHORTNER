# Module 1 Reflection: Code Review as Communication

## 1. Review Style Decision

I chose **summary review** (Option B) because the PR scenario involved an analytics dashboard with multiple concerns: a critical runtime bug, a secondary crash path, and a data-integrity edge case. A summary review lets me structure the feedback top-down — most critical first — so the author sees the fire before the furniture.

For a **15-file PR**, I would absolutely use summary review with a high-level overview of architectural concerns followed by per-file notes only where needed. For a **single 5-line function**, inline comments might be faster, but I would still open with a one-sentence summary so the author knows whether the change is a "fix and merge" or a "rethink the approach."

## 2. Tone and Effectiveness

The hostile review and the constructive review both noticed the same surface-level issues (naming, missing docstring). But the hostile review buried the division-by-zero bug in a wall of sarcasm, so the author skimmed past it. The constructive review placed the bug at the top, labeled it critical, and paired it with a code snippet.

**Takeaway:** Tone is not decoration — it is a sorting mechanism. When reviewers are angry, authors get defensive and stop reading carefully. When reviewers are kind, authors stay receptive long enough to absorb the technical substance. A technically perfect review that the author ignores is **worse** than a slightly imperfect review that the author acts on.

## 3. Gatekeeping vs. Collaboration

I want to **practice** collaboration. Gatekeeping is faster in the moment ("reject and move on"), but it creates a culture where people stop sharing drafts, stop asking questions, and start gaming the review system. Collaboration is slower because it requires explaining *why* something matters, but it compounds: authors learn from the feedback loop and write better code in the next PR.

I want to **receive** collaboration too. The reviews that made me a better engineer were the ones that said, "Here is a pattern you might not know about," not the ones that said, "This is wrong."

---

**What we shipped:** A code review that is specific, kind, and actionable.
**What we learned:** Communication style determines whether technical observations actually improve the code.
