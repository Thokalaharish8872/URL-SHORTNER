# Flawed Stakeholder Communication Analysis

## Part 1: Count the Jargon

**Jargon terms (20+ found):**
1. EOL (end of life) - undefined
2. Kong (software product) - undefined
3. 2.8.x (version number) - undefined
4. NGINX reverse proxy - undefined
5. Lua plugins - undefined
6. mTLS termination - undefined
7. zero-trust policies - undefined
8. east-west - undefined
9. tech debt - undefined
10. autoscaling group - undefined
11. c5.2xlarge instances - undefined
12. RPS (requests per second) - undefined
13. p95 (95th percentile latency) - undefined
14. p99 (99th percentile latency) - undefined
15. SLO (service level objective) - undefined
16. Envoy-based ingress - undefined
17. Kubernetes clusters - undefined
18. service mesh - undefined
19. Istio sidecars - undefined
20. circuit breaking - undefined
21. retry budgets - undefined
22. WASM filters - undefined
23. CI/CD pipelines - undefined
24. GitOps - undefined
25. observability stack - undefined
26. StatsD - undefined
27. Grafana - undefined
28. OpenTelemetry collectors - undefined
29. Datadog tenant - undefined
30. blue-green deployment - undefined
31. synthetic load tests - undefined

The email is nearly unintelligible to a non-technical stakeholder.

## Part 2: Find the Buried Risk

**The buried risk:**
During Black Friday last November, the checkout service failed for 47 minutes, causing the company to miss its 99.95% availability target and dropping to 99.2%. This likely resulted in significant lost revenue during the highest-traffic shopping period of the year.

**Plain sentence that would make David sit up:**
"Last Black Friday, our checkout service failed for 47 minutes during peak shopping hours, costing us significant revenue that we don't want to repeat."

The risk is buried in the second paragraph of the "Background" section, wrapped in technical metrics (11,400 RPS, p99 spike to 1.8 seconds, 99.2% availability) that hide the business impact.

## Part 3: Where is the Ask?

**Current closing:** "Let me know if you have questions" - not an ask, just a polite dismissal.

**What Marcus should actually be asking for:**
1. Approval to proceed with the 8-week infrastructure migration project requiring 2 engineers
2. Approval for the additional cluster memory (42.5 GB) needed for Istio sidecar overhead
3. Approval for the risk of running both systems in parallel during the migration window
4. A decision on whether to proceed given the Black Friday performance risk if WASM filters don't perform as expected

Marcus needs decisions on budget (engineering time, infrastructure costs), timeline (8-week migration window), and risk acceptance (performance during migration). None of these are requested in the email.
