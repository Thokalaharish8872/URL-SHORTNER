# Module 1 Reflection: AI Engineering Mindset

## Comprehension Questions

### 1. What core problem does this module solve in the AI engineering mindset?
The module solves the problem of trusting AI agent outputs without verification. It teaches that the AI generates and the human decides - every line of code the AI produces becomes your code when you accept it. The core problem is that AI agents can hallucinate or make assumptions based on typical patterns rather than actual codebase realities. The solution is a trust-but-verify workflow: get the agent's output, pause to assess what you trust vs what needs verification, run targeted verification commands, and document discrepancies.

### 2. Which decision in this module has the biggest impact, and why?
The delegation strategy decision (full autopilot vs task-by-task vs hybrid) has the biggest impact. I chose task-by-task because the codebase is unfamiliar and the feature is complex. Wrong assumptions early cascade through all subsequent work. Task-by-task catches errors after 30 lines instead of discovering them after 500 lines across 12 files. The cost of fixing a wrong assumption early (redo one task) is much lower than fixing it late (potentially redo all eight). This decision affects every module going forward - how I delegate work to AI agents determines whether I catch errors early or ship broken code.

### 3. What evidence proves the implementation works end-to-end?
Verification evidence: Ran three verification commands against the agent's architecture summary claims. `ls src` verified directory structure (models, routes, services exist). `cat src/models/store.js` verified data models (users, teams, invitations arrays). `cat src/routes/index.js` verified routes (GET /health, GET /teams). All factual claims about the starter workspace matched actual files. Found discrepancy when comparing to parent CAW Assessment project - agent described the starter workspace accurately, but the actual project uses Python FastAPI with PostgreSQL, not Node.js with in-memory storage. Created corrected architecture summary and documented the root cause (insufficient context - created wrong workspace). This proves the trust-but-verify workflow caught the error.

## Mini Practical Task

### STEP 4 Verification: Trust Audit Commands

**Task**: Run verification commands to validate agent's architecture summary claims

**Commands**:
```bash
ls src
# Output: models, routes, services directories exist ✓

cat src/models/store.js
# Output: export const users = []; export const teams = []; export const invitations = []; ✓

cat src/routes/index.js
# Output: export function listRoutes() { return ["GET /health", "GET /teams"]; } ✓
```

**Proof**: All verification commands confirmed the agent's factual claims about the starter workspace structure were accurate. Discovered discrepancy when checking parent project - agent described created workspace accurately, but actual CAW Assessment project uses different stack. Trust audit documented in trust-audit.md with verification results and corrected summary.

## Risk and Mitigation

### Risk
**Insufficient context leading to wrong workspace**: I created a new Node.js starter workspace instead of using the existing CAW Assessment project (Python FastAPI with PostgreSQL). The agent accurately described what I gave it, but this was not the intended target. If building features for the actual project, the summary would be misleading. Wrong assumptions about the tech stack would cause all subsequent prompts to be based on incorrect foundations.

### Mitigation
**Check for existing applications before creating starter workspace**: Always verify whether there's an existing application directory (api/, src/, app/) before creating a new starter workspace. If a real application exists, use it instead. This is a "fixable with better context" issue - the agent did its job correctly, but I gave it the wrong context. Better initial context prevents this entire class of errors.

## Key Takeaways

1. **The AI generates, the human decides**: Every line of AI-generated code becomes your code when you accept it. Security holes and production incidents are your responsibility, not the AI's.
2. **Trust-but-verify workflow**: Get agent output, pause to assess trust vs verification needs, run targeted verification commands, document discrepancies. Build calibrated sense of when agent is accurate vs guessing.
3. **80/20 split**: AI gets you 80% of the way in 20% of time (scaffold, boilerplate, straightforward logic). The remaining 20% (review, edge cases, security, integration) takes 80% of effort - that's where engineering skill lives.
4. **Delegation strategy matters**: Task-by-task catches errors early for unfamiliar codebases or complex features. Full autopilot works for well-understood, isolated tasks. Wrong assumptions cascade - catch them before they compound.
5. **Insufficient context is the most common error**: Agent hallucinations often come from not being pointed at the right files or being asked to describe code it hasn't seen. Better prompts with specific file paths and targeted questions fix this.
