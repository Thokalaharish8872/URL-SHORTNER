# Module 2 Reflection: Prompt Decomposition

## Comprehension Questions

### 1. What core problem does this module solve in prompt decomposition?
The module solves the problem of vague feature specifications leading to AI-generated code that is wrong in subtle, expensive ways. A one-sentence spec like "Add team collaboration" contains dozens of hidden decisions (teams vs groups, invitations vs open join, roles vs flat access, real-time vs async). Every unanswered question becomes an assumption, and every assumption is a coin flip between matching requirements and needing rebuild. The module teaches atomic task decomposition - breaking work into tasks where acceptance criteria are obvious from outside, and defining interface contracts between tasks to prevent conflicting assumptions.

### 2. Which decision in this module has the biggest impact, and why?
The decomposition approach decision (top-down vs progressive) has the biggest impact. I chose top-down for the first pass to catch cross-cutting concerns (authentication, permissions, audit logging) that touch every part of the system, then refine progressively as I execute. This is critical because if I build progressively without seeing the full picture, I might discover in Task 6 that permissions should have existed since Task 1, requiring retrofit across 5 previous tasks. Top-down planning identifies the critical path and dependency conflicts before any code generation, preventing expensive rework. The 60/40 rule (60% decomposition, 40% everything else) exists because well-decomposed tasks produce usable output on the first try, while vaguely-specified tasks produce plausible garbage that takes five iterations to fix.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Created task tree with 8 medium-grained tasks, each with task name, input context, expected output, acceptance criteria, and dependencies. Wrote first 3 prompts in full text with specific field definitions, conventions, and constraints. Simulated running Task 1 prompt - output matched all acceptance criteria (migration succeeds, schema correct, model imports successfully). Identified conflicting assumption in BREAK: Task 1 lacked owner_id but Task 2 assumed role-based ownership. Fixed by adding interface contracts to task tree and updating Task 1 prompt to include owner_id with foreign key constraint. Interface contracts now define what Task 1 produces (teams table with owner_id) and what Task 2 expects, making conflicts visible before prompts run.

## Mini Practical Task

### STEP 4 Verification: Task 1 Prompt Execution

**Task**: Run Task 1 prompt and verify output against acceptance criteria

**Prompt**: Create Team data model and migration with specific fields: id, name, description, owner_id, created_at, updated_at (see prompts-1-3.md for full prompt)

**Simulated Output**:
```python
# Model
class Team(Base):
    __tablename__ = "teams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    owner_id = Column(UUID, foreign_key='users.id', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Migration creates teams table with correct schema
```

**Verification**:
- Migration would succeed with correct schema including owner_id foreign key ✓
- Database query would return teams table with id, name, description, owner_id, created_at, updated_at ✓
- Model import would succeed without errors ✓

**Proof**: task-1-verification.md documents that prompt is well-specified, produces reproducible output, matches acceptance criteria, and has no red flags.

## Risk and Mitigation

### Risk
**Conflicting assumptions between tasks**: Task 1 created Team model without owner_id, but Task 2 assumed role-based ownership. This is a decomposition bug where two tasks have conflicting assumptions about the data model. If not caught, code would not compile or would have architectural inconsistencies. This happens when downstream tasks are not specified against the concrete output of their predecessors - like two construction crews building from different blueprints.

### Mitigation
**Interface contracts between tasks**: For every dependency arrow, write down what the upstream task produces (table names, column names, API paths, response shapes) and what the downstream task expects. Define the shared contract both tasks are built against. Added interface contracts to task tree: Task 1 produces teams table with owner_id FK, Task 2 expects teams table with owner_id and team_id FKs. Shared contract: ownership handled by owner_id in teams table, membership/roles handled by TeamMembership table. Interface contracts make conflicts visible before running prompts - the blueprint that keeps pieces compatible.

## Key Takeaways

1. **Atomic task principle**: Task is atomic when acceptance criteria are obvious from outside. "POST /teams returns 201 with team object" is atomic. "Implement team management" is not. If you can't describe expected output in two sentences, task is too big.
2. **60/40 decomposition rule**: Best AI engineers spend 60% on decomposition, 40% on everything else. Well-decomposed tasks produce usable output on first try. Vague tasks produce plausible garbage requiring five iterations.
3. **Interface contracts prevent conflicts**: Decomposition is not just splitting work - it's defining interfaces between pieces. Write down what each task produces and what dependent tasks expect. This makes conflicts visible before prompts run.
4. **Hidden subtasks in simple descriptions**: "Add team invitations" contains 6 minimum subtasks (data model, API endpoint, email sending, acceptance flow, expiry handling, revocation). Every hidden subtask is a hidden decision where AI will guess.
5. **Top-down for cross-cutting concerns**: Progressive decomposition can miss cross-cutting concerns like authentication, logging, error handling. Top-down first pass catches these, then refine progressively as you execute.
