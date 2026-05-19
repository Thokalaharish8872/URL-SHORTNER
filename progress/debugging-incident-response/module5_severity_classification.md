# Module 5 Micro-Exercise: Severity Classification

## Severity Levels

**SEV1** (House fire): Service down, data being lost, active security exploitation. All hands on deck. External communication required. Wake people up at 3 AM.

**SEV2** (Grease fire): Major feature broken, security vulnerability with active exploitation but limited blast radius. Dedicated responder, status updates to leadership, but don't page entire company.

**SEV3** (Campfire): Minor degradation, cosmetic issues, potential problem not causing harm yet. Fix during business hours. Track it. Don't cancel dinner.

## Friday Afternoon Disaster Pattern
Company discovers potential security vulnerability Friday at 4 PM. On-call engineer panics, pushes hasty fix directly to production without triaging. Fix has typo in auth middleware - login broken for ALL users. Original vulnerability was low-severity edge case affecting 0.1% of requests. Rushed fix caused SEV1 outage, original bug was SEV3.

**Lesson**: Triage first, then fix. Five minutes classifying the problem saves you from turning a campfire into a house fire.

## Scenario Classifications

### 1. Homepage loads but all images are broken
**Classification**: SEV2 or SEV3 (depends on business context)

**Reasoning**: 
- For e-commerce site where images ARE the product: SEV2 - customers cannot evaluate what they're buying, major revenue impact
- For internal tool: SEV3 - cosmetic issue, doesn't prevent core functionality
- Context matters - severity depends on business impact

### 2. Users can see other users' private data when changing URL parameter
**Classification**: SEV1

**Reasoning**: This is a data breach. Users accessing other users' private data is a security incident with regulatory implications (GDPR, CCPA). Active exploitation in progress. Drop everything, external communication required, legal team notification needed.

### 3. Background analytics job generating weekly reports delayed by 2 hours
**Classification**: SEV3

**Reasoning**: Reports are delayed, not lost. No users directly affected in real time. Fix during business hours. If it were a real-time billing job, classification would change to SEV2 or SEV1 depending on business impact.

## Key Takeaways

1. **Triage before fixing**: Five minutes classification prevents turning SEV3 into SEV1
2. **Context matters**: Same technical issue can be different severity based on business impact
3. **Security incidents are SEV1**: Data breaches and active exploitation require immediate escalation
4. **Don't panic under pressure**: Friday afternoon disasters happen when people skip triage and rush fixes
5. **Severity determines response**: Who to notify, how fast to communicate, whether to escalate
