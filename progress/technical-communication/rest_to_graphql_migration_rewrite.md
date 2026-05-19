# REST to GraphQL Migration

We are migrating our API from REST to GraphQL to reduce frontend API calls by 40% and eliminate 15 aggregation endpoints.

## Why This Change

Our frontend (FE) team spends 30% of sprint capacity building custom aggregation endpoints. Mobile and web clients need different data shapes from the same entities, creating many endpoints to maintain.

We evaluated three options:
1. Keep REST with a Backend-for-Frontend (BFF) service - rejected due to operational complexity
2. Keep REST with standardized schemas - rejected, doesn't solve the data shape mismatch
3. Migrate to GraphQL - selected

## What Is GraphQL

GraphQL is a query language that lets clients request exactly the data they need, instead of getting a fixed response from the server. Think of it like a buffet instead of a fixed menu.

## The Plan

Three engineers will work full-time on the migration for 8 weeks. Two are learning GraphQL. The REST API and GraphQL endpoint will run simultaneously during the transition.

## Risks

- **Query performance:** The backend team will track query performance daily during the first two weeks
- **Caching complexity:** We will use a GraphQL-specific caching layer

## Impact

The Software Development Kit (SDK) team will benefit from simplified API versioning. The Site Reliability Engineering (SRE) team will see reduced latency from fewer sequential calls.

## Timeline

The timeline may shift during implementation. The backend team will communicate changes to all stakeholders.
