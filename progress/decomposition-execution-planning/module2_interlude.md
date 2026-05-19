# Healthcare.gov Interlude Reflection

## Question 1: Why weren't 55 separate project plans enough?

Each contractor's plan described their own work in detail but missed the connections between the parts. A single dependency graph spanning all 55 teams would have made visible:

- **Interface contracts:** What data formats, error codes, and handoff points exist between systems (e.g., identity verification to eligibility engine)
- **Integration dependencies:** Which systems must work together for end-to-end functionality
- **Bottlenecks:** Where load balancing needed to be system-wide, not per-component
- **Critical path:** The minimum set of systems that must work for a single user to enroll

Individual plans show you what each piece does. A dependency graph shows you how the pieces fit together - and where the gaps are that will cause collapse.

## Question 2: What's the FIRST thing you'd do on Day 2?

Map the system. Draw the dependency graph showing every data flow from user's browser through every backend service and back. Identify:

- Which connections are broken
- Which services are bottlenecks
- Which failures are cascading into other failures
- The critical path - the thinnest possible path through the system that results in one person getting health insurance

You cannot fix what you don't understand. Before touching a single bug, you need a map of how the system actually works together, not how each contractor thought it worked in isolation.
