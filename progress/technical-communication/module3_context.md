# Module 3 Context: Design Documents

## Micro-Exercise Answers

1. **Time I realized the approach was wrong halfway through:**
   When building the analytics dashboard API, I implemented a caching layer using Redis without first consulting the infrastructure team. Halfway through, I discovered they had a company-wide caching service with specific requirements (consistent hashing, multi-region sync) that my implementation didn't comply with. I had to rewrite the entire caching layer.

2. **Minimum document to get useful feedback:**
   A one-page proposal with: problem statement, proposed solution, infrastructure requirements, and estimated timeline. That's enough for the relevant teams to flag issues like infrastructure limitations, security concerns, or timeline conflicts before any code is written.
