# Module 5 Reflection: Iteration Patterns

## Comprehension Questions

1. What core problem does this module solve in iteration patterns?
AI agent iteration can spiral into context pollution - accumulated conversation tokens cause agent to compromise between all requests instead of implementing what's needed. Two-iteration rule: if not converging after 2 refinements, restart. Distinguishing surface vs structural issues critical - surface fixes refine, structural flaws restart. Quality trajectory is data - trust it, not hope.

2. Which decision in this module has the biggest impact, and why?
Refine vs restart decision has biggest impact. Restart-early strategy with two-iteration threshold prevents wasted iterations on structural flaws. Context pollution makes later iterations worse, not better. Knowing when to stop iterating is as important as how to iterate. Persistence past convergence point actively harms output quality with AI agents.

3. What evidence proves the implementation works end-to-end?
Iteration log shows trajectory: Round 1 (2,3) restart -> Round 2 (4,2) refine -> Round 3 (4,3) refine -> Round 4 (4,4) ship. Healthy trajectory: structural held steady, surface improved. Functional verification: connection succeeds, event delivery works, disconnection cleans up, reconnection resubscribes and replays events. WebSocket activity feed ships within 4-iteration budget.

## Mini Practical Task

STEP 4 verification: Trajectory analysis from iteration log.
- Round 1: structural 2, surface 3 (baseline)
- Round 2: structural 4, surface 2 (improving after restart)
- Round 3: structural 4, surface 3 (improving)
- Round 4: structural 4, surface 4 (shipped)

Quality converged upward. Two-iteration rule prevented spiral on regression.

## Risk and Mitigation

Risk: Context pollution causes regression - agent optimizes for latest instruction at expense of earlier achievements. Spiral where later iterations break previously working features.

Mitigation: Two-iteration rule with restart threshold. Quality trajectory tracking - if not converging after 2 refinements, restart. Fresh conversations produce cleaner output than polluted ones. Specific constraints in restart prompt prevent repeating same mistakes.

## Key Takeaways

1. Surface vs structural issues: surface fixes refine, structural flaws require restart
2. Two-iteration rule: if not converging after 2 refinements, restart
3. Context pollution is real - accumulated conversation causes regression
4. Quality trajectory is data - trust it, don't hope
5. Knowing when to stop iterating is as important as how to iterate
6. Restart prompts should incorporate everything learned from failed iterations
