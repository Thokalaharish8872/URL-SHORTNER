# Module 1 Micro-Exercise: Hypothesis-First Debugging

## Scenario
Web service returns a 500 error. No code has been examined yet. No logs have been read.

## Two Possible Causes

### Cause 1: Database Connection Failure
**Explanation**: The application cannot connect to the database, causing an unhandled exception when trying to query data.

**Test to Confirm/Rule Out**: 
- Command: `psql -h localhost -U username -d dbname -c "SELECT 1"`
- Or: Check database logs for connection errors
- Or: `docker ps` to verify database container is running

**What this tells us**: If the connection succeeds, the database is available and the cause is ruled out. If it fails, database connectivity is the issue.

### Cause 2: Missing Environment Variable
**Explanation**: A required environment variable (e.g., DATABASE_URL, API_KEY) is not set, causing the application to fail on startup or when accessing configuration.

**Test to Confirm/Rule Out**:
- Command: `env | grep DATABASE_URL` (or specific variable name)
- Or: `printenv` to list all environment variables
- Or: Check .env file for missing required variables

**What this tells us**: If the variable is present and valid, configuration is not the issue. If missing or invalid, this is the cause.

## Key Insight
Before touching any code, I:
1. Observed the symptom (500 error)
2. Formed two hypotheses (database failure, missing config)
3. Identified specific tests for each hypothesis

This is hypothesis-first debugging - thinking before acting. Each test either confirms or eliminates a possibility, converging on the root cause without reading irrelevant code or making random changes.
