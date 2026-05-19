# Module 2 Reflection: Dependency Mapping

## Comprehension Questions

1. **What core problem does this module solve in dependency mapping?**
   This module teaches how to turn a flat list of requirements into a dependency graph (DAG) that shows build order, identifies parallel tracks, and finds the critical path. It teaches distinguishing hard vs soft dependencies, detecting circular dependencies, and breaking cycles by splitting nodes into minimal and full versions.

2. **Which decision in this module has the biggest impact, and why?**
   The critical path strategy decision has the biggest impact because it determines the minimum project duration. If you accept the critical path, you optimize around it. If you actively shorten it by splitting items, you can dramatically reduce project duration by unlocking parallelism that was previously blocked.

3. **What evidence proves the implementation works end-to-end?**
   The dependency graph with 13 work items, labeled hard/soft dependencies, identified starting points (Auth, Provider Onboarding), endpoints (Notification System, Admin Dashboard), and critical path (11 items). The graph fixed a circular dependency by splitting Admin Dashboard into Admin Review Tool (Minimal) and Admin Dashboard (Full), demonstrating cycle detection and resolution.

## Mini Practical Task

**STEP 4 verification for dependency mapping:**

**Verification action:** Checked that the graph has multiple starting points (Auth, Provider Onboarding) not a single bottleneck root. Verified parallel tracks exist (Search, Review System can run independently of critical path items). Applied double time test to Payment Processing - it delays 4 downstream items but parallel tracks remain unaffected, showing resilient plan structure.

**Proof:** The dependency graph shows two starting points, multiple parallel tracks (Search & Browse, Review System, Provider Onboarding), and hard/soft dependency labels distinguishing constraints from preferences. Critical path analysis identified 11-item chain with 21-day minimum timeline.
