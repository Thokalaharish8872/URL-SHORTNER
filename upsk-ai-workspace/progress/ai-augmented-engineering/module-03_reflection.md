# Module 3 Reflection: Context Engineering

## Comprehension Questions

### 1. What core problem does this module solve in context engineering?
The module solves the problem that context selection determines output quality more than prompt wording. An AI agent with too much context (40 files when only 3 are relevant) averages across irrelevant patterns and mixes conventions. An agent with too little context invents its own patterns that don't match the codebase. Context engineering is about selecting the right files - the architectural context (project conventions always included), local context (task-specific files), and constraint context (do-not rules). The key insight: the agent doesn't know your conventions unless you show them explicitly - every convention must be present in the context window or it doesn't exist for the agent.

### 2. Which decision in this module has the biggest impact, and why?
The context strategy decision (kitchen sink vs surgical vs layered) has the biggest impact. I chose surgical with architectural documentation - hand-picking exactly the files agent needs per task while maintaining a reusable architectural context document. This gives maximum signal-to-noise ratio while ensuring conventions are followed. Kitchen sink includes too much noise - agent averages across irrelevant patterns. Surgical alone risks missing critical conventions if codebase not deeply understood. Layered approach (architectural context always + local context curated per task + constraint context as system instructions) combines strengths: consistency from architectural doc, precision from surgical selection, safety from constraints.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Created system-level context document for CAW Assessment project documenting architecture (Python FastAPI, SQLAlchemy, Pydantic, Alembic, Celery, Redis), coding conventions (naming, file naming, error handling, validation, authentication), and constraints (no new dependencies, use existing auth, error format, file conventions, database changes with migrations). Created per-task context bundles for Tasks 1-3 with files to read (with "if omitted" reasoning), files to modify, expected output format. Identified convention violation in BREAK: Task 3 error response format mismatch. Fixed by adding concrete HTTPException example to system-context.md and updating Task 3 context bundle to explicitly reference error handling section. This proves context was the problem - prompt didn't change, only context changed, and output quality changed with it.

## Mini Practical Task

### STEP 4 Verification: Context Package Improvement

**Task**: Identify missing context and add concrete example to fix convention violation

**Original Context**: System-level context described error format textually: `{"detail": "Error message here"}`

**Violation Found**: Agent produced `{"status": "error", "message": "...", "statusCode": 400}` instead of `{"detail": "message"}`

**Fix Applied**: Added concrete example to system-context.md:
```python
from fastapi import HTTPException

# For not found
raise HTTPException(status_code=404, detail="Link not found")

# For validation errors
raise HTTPException(status_code=422, detail="Team name is required")
```

**Result**: Updated Task 3 context bundle to explicitly reference system-context.md Error Handling section with warning not to use status/statusCode/code fields. This ensures agent follows exact error format.

**Proof**: system-context.md and task-3-context.md updated with concrete examples and explicit constraints.

## Risk and Mitigation

### Risk
**Vague architectural context produces vague compliance**: System-level context document described error handling pattern textually but lacked concrete code example. Agent inferred pattern and chose different but "reasonable" format. This creates API inconsistency - clients expecting one format from existing endpoints break when calling new endpoints. Architectural context is not optional - agent pattern-matches against training data, not your project. Your project's patterns only exist in context window.

### Mitigation
**Add concrete code examples to architectural context**: Instead of describing patterns textually, show actual code snippets demonstrating the pattern. Make constraints explicit: "MUST use HTTPException with detail parameter. Do NOT use status, statusCode, or code fields." Show example usage from existing codebase. Context engineering requires being almost comically direct - the agent doesn't know your project unless shown explicitly. Every convention must be present in context every single time.

## Key Takeaways

1. **Context selection > prompt wording**: A mediocre prompt with excellent context outperforms a brilliant prompt with poor context. Context window is like briefcase - pack what matters for specific problem.
2. **Context triangle has three layers**: Architectural context (how we do things here - always included), Local context (task-specific files - curated per task), Constraint context (do-not rules - system-level instructions).
3. **Agent doesn't know your project**: Agent pattern-matches against training data, not your codebase. Your project's patterns only exist in context window. If not there, they don't exist for agent.
4. **Concrete examples > textual descriptions**: Describing error format as `{"detail": "message"}` is not enough. Show actual code: `raise HTTPException(status_code=404, detail="Link not found")`. Agent needs explicit examples.
5. **"If omitted" reasoning forces justification**: For each file in context bundle, state what goes wrong if omitted. This forces critical thinking about context cost vs value and prevents missing critical files.
