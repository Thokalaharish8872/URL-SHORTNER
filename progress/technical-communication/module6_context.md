# Module 6 Context: Documentation

## Micro-Exercise Answers

1. **Could a new hire run the project locally using only the README?**
   No. Most READMEs I've seen are out of date within months of being written. They describe the initial setup but don't account for dependency changes, environment variable additions, or configuration shifts that happen over time. A new hire following the README would encounter errors that require asking someone or debugging the setup process.

2. **When was the last time anyone verified that the steps still work?**
   Rarely, if ever. Teams write READMEs during initial setup and never revisit them unless something breaks catastrophically. The GitLab story is typical: the backup tool changed from pg_dump to LVM snapshots, but nobody updated the runbook. Without a process to periodically verify documentation accuracy, it inevitably becomes stale.

The GitLab incident illustrates the core problem: wrong documentation is worse than no documentation because it wastes time and gives false confidence. Following stale steps during an emergency is catastrophic.
