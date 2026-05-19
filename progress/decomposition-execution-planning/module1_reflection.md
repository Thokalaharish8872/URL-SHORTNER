# Module 1 Reflection: Reading Requirements

## Comprehension Questions

1. **What core problem does this module solve in reading requirements?**
   This module teaches how to extract explicit, implicit, and conflicting requirements from ambiguous prose. It teaches finding what's missing (the "silence pass"), identifying contradictions between spec sections, and proposing concrete solutions rather than just flagging problems.

2. **Which decision in this module has the biggest impact, and why?**
   The extraction structure decision (flat list vs categorized matrix) has the biggest impact because it determines how useful the document is later. Categorized matrix makes gaps visible by stakeholder and type, allowing faster answers to stakeholder questions and better work estimation for engineers.

3. **What evidence proves the implementation works end-to-end?**
   The full requirements extraction (22 requirements across USER/PROVIDER/PLATFORM stakeholders with functional/constraint/quality attribute types) plus identification of cancellation contradiction with two resolution options demonstrates the implementation works. The document includes 12 flagged ambiguities and identifies 5 requirements affected by the blocked cancellation decision.

## Mini Practical Task

**STEP 4 verification for requirement extraction:**

**Verification action:** Checked that I extracted more than 12 requirements (found 22) and that I separated "browse by category" and "view profiles" as distinct requirements since they imply different UI, data, and search/filter behavior. Also extracted "ratings" as separate from "profiles" since a rating system needs its own data model, submission flow, display format, and abuse prevention.

**Proof:** The requirements document contains 22 distinct requirements with type, stakeholder, source, and confidence ratings for each, demonstrating I read beyond surface level to find what's between the lines.
