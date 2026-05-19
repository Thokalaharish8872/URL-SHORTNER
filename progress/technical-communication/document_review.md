# Document Review: ShopStream REST-to-GraphQL Migration

## Total Problems Found: 15

---

## 1. Buried Lede

**Problem:** "As many of you are aware, the backend team has been evaluating several potential approaches to addressing some of the challenges that have been encountered with our current API infrastructure over the past few months."

**Category:** Buried lede

**Why it's a problem:** The reader has to read through 43 words before reaching any meaningful information. The actual decision ("we are migrating from REST to GraphQL") doesn't appear until the fourth paragraph. A busy reader might never get there.

---

## 2. Passive Voice

**Problem:** "After extensive deliberation and analysis of various factors including developer velocity, client-side performance metrics, and long-term maintainability considerations, a decision has been reached regarding the future direction of our API strategy."

**Category:** Passive voice

**Why it's a problem:** "A decision has been reached" hides who made the decision. The reader doesn't know who owns this change.

---

## 3. Passive Voice

**Problem:** "It should be noted that the existing system, while functional, has presented certain inefficiencies that have been identified by multiple teams."

**Category:** Passive voice

**Why it's a problem:** "It should be noted that" is filler that adds no information. "Has been identified by multiple teams" hides which teams identified the issues.

---

## 4. Passive Voice

**Problem:** "BFF patterns were considered as an alternative but were ultimately deemed to introduce unacceptable operational overhead in terms of deployment complexity and monitoring requirements."

**Category:** Passive voice

**Why it's a problem:** "Were considered" and "were deemed" hide who made the evaluation and decision.

---

## 5. Jargon Without Definition

**Problem:** "BFF patterns"

**Category:** Jargon

**Why it's a problem:** Priya, a new engineer, would not know what "BFF" means without context (Backend-for-Frontend). The term is used without explanation.

---

## 6. Passive Voice

**Problem:** "The mobile team has been particularly impacted by the current architecture."

**Category:** Passive voice

**Why it's a problem:** "Has been impacted" is vague. How are they impacted? What specifically is the problem?

---

## 7. Wordiness

**Problem:** "Different data shapes are required by the mobile and web clients for what are essentially the same underlying data entities, resulting in the proliferation of purpose-built endpoints that must be individually maintained, tested, and monitored."

**Category:** Wordiness

**Why it's a problem:** This 33-word sentence could be much shorter. "Mobile and web clients need different data shapes from the same entities, creating many endpoints to maintain."

---

## 8. Passive Voice

**Problem:** "The SDK team has also expressed concerns about the current approach to API versioning, noting that backwards compatibility has been difficult to maintain across the growing number of endpoints."

**Category:** Passive voice

**Why it's a problem:** "Has been difficult to maintain" hides what makes it difficult and who is struggling.

---

## 9. Jargon Without Definition

**Problem:** "SDK team"

**Category:** Jargon

**Why it's a problem:** Priya might not know what the SDK team does or why they care about API versioning.

---

## 10. Jargon Without Definition

**Problem:** "SRE team"

**Category:** Jargon

**Why it's a problem:** Priya might not know what SRE (Site Reliability Engineering) means or their role in the organization.

---

## 11. Passive Voice

**Problem:** "Given these considerations, the team has decided to migrate from REST to GraphQL."

**Category:** Passive voice

**Why it's a problem:** "The team has decided" is acceptable, but it's still slightly vague. Which team? Who specifically made the call?

---

## 12. Passive Voice

**Problem:** "It is expected that this migration will result in an approximately 40% reduction in frontend API calls and the elimination of 15 aggregation endpoints that will no longer be needed."

**Category:** Passive voice

**Why it's a problem:** "It is expected that" is filler. "Will no longer be needed" hides who will deprecate the endpoints and when.

---

## 13. Passive Voice

**Problem:** "Three engineers have been allocated to the project for a period of approximately 8 weeks."

**Category:** Passive voice

**Why it's a problem:** "Have been allocated" hides who allocated them and why these three specifically.

---

## 14. Passive Voice

**Problem:** "Regarding risks, it has been acknowledged that query performance unpredictability and caching complexity are areas of concern."

**Category:** Passive voice

**Why it's a problem:** "It has been acknowledged that" is filler. Who acknowledged this? What exactly is the concern?

---

## 15. Ambiguity

**Problem:** "These risks will be monitored closely and addressed as they arise."

**Category:** Ambiguity

**Why it's a problem:** By whom? How? What counts as "closely"? When exactly? This provides no actionable information.

---

## 16. Ambiguity

**Problem:** "Stakeholders should be aware that the timeline is subject to adjustment based on findings during the implementation phase."

**Category:** Ambiguity

**Why it's a problem:** Which stakeholders? What constitutes "findings"? Under what conditions would the timeline adjust? This is vague and unhelpful.

---

## 17. Structure

**Problem:** No headings, no bullet points, no visual structure

**Category:** Structure

**Why it's a problem:** The document is a wall of text. Priya cannot skim it to find what she needs. She must read every word to understand the shape of the content.

---

## 18. Wordiness

**Problem:** "As many of you are aware"

**Category:** Wordiness

**Why it's a problem:** Filler that adds no information. Remove it entirely.

---

## 19. Wordiness

**Problem:** "evaluating several potential approaches to addressing some of the challenges"

**Category:** Wordiness

**Why it's a problem:** Could be "evaluating approaches to API challenges."

---

## 20. Wordiness

**Problem:** "over the past few months"

**Category:** Wordiness

**Why it's a problem:** Could be "recently."

---

## 21. Wordiness

**Problem:** "After extensive deliberation and analysis of various factors"

**Category:** Wordiness

**Why it's a problem:** Could be "After evaluating developer velocity, performance, and maintainability."

---

## 22. Wordiness

**Problem:** "it should be noted that"

**Category:** Wordiness

**Why it's a problem:** Filler. Remove it entirely.

---

## Summary

**Total problems identified: 22**

The document fails the reader at every turn:
- **Structure:** No headings, no bullets, wall of text
- **Passive voice:** 11 instances hiding accountability
- **Buried lede:** Main point appears in paragraph 4
- **Jargon:** 3 undefined acronyms (BFF, SDK, SRE)
- **Wordiness:** 6 instances of unnecessary filler
- **Ambiguity:** 2 vague statements with no actionable information

The author is smart and the facts are correct, but the writing actively works against the reader.
