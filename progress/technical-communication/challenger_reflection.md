# Challenger Disaster Reflection

## Reflection Questions

1. **When is being technically correct not enough?**
Being technically correct is not enough when the audience doesn't speak your technical language or doesn't share your priorities. Boisjoly had the right data and the right conclusion, but he presented it in engineering terms to managers whose frame was schedule pressure and public credibility. Effective communication requires translating technical accuracy into the audience's decision framework - what they care about, what they fear, what they value. Being right is necessary but insufficient; you must also be persuasive in your audience's language.

2. **How would you reframe "our deployment pipeline lacks a canary stage" for budget/timeline-focused stakeholders?**
For stakeholders focused on budget and timeline, I would reframe it as: "Without a canary stage, we risk deploying breaking changes to all customers at once. Last year, a similar deployment caused 4 hours of downtime, cost $50K in refunds, and required the entire engineering team to work through the weekend. A canary stage adds 2 hours to deployment time but reduces the blast radius from all customers to 1%, and lets us catch issues before they affect revenue. The risk of not having it is a catastrophic outage; the risk of adding it is minimal delay."

The language changes from technical ("canary stage") to business impact (revenue, refunds, weekend work). The emphasis shifts from technical architecture to risk management and cost.

3. **Where is the line between "we need better communication skills" and "we need better processes"?**
Both are needed, but they serve different purposes. Better communication skills help you get the right decision in the moment when stakes are high and time is short. Better processes provide safety nets when communication fails or when the stakes are routine. Boisjoly's persuasion skills might have prevented the disaster that night, but NASA still needed escalation procedures so that any engineer (not just the most persuasive) could halt a launch on safety grounds. Processes cannot replace the need for persuasive communication in high-stakes, time-constrained situations, and communication skills cannot replace the need for systematic safeguards. You need both.
