# Extension Points Prompt

Identify the extension points in this codebase. An extension point is a place in the code designed to accept new functionality.

Specifically identify:
1. Where would new API routes go? Is there a file-per-route pattern, or are they all in one file?
2. Where would new data models be defined? Is there a models directory with one file per model?
3. Is there a pattern for adding middleware - code that runs on every request before it reaches the route handler?
4. Is there a pattern for background jobs or async work - tasks that happen behind the scenes?

This analysis will help ensure that when we add new features, we follow the existing patterns in the codebase.
