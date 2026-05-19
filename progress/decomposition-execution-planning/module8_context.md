# Module 8 Context: Integration Bugs

## Micro-Exercise: Find the Integration Bug

**The Bug:** created_at type mismatch between Booking Service and Notification Service

**Booking Service API:**
- Sends created_at as ISO 8601 string: "2025-03-15T14:30:00Z"

**Notification Service API:**
- Expects created_at as Unix timestamp (number): 1710513000

**Why this causes integration failure:**
When Booking Service sends a date string to Notification Service expecting a number, the notification service either:
- Crashes (if it tries to parse the string as a number)
- Sends an email with the wrong date (if it defaults to epoch or current time)
- Silently drops the field (if it rejects invalid input)

**Both specs are individually correct:**
- ISO 8601 is a valid date format for Booking Service
- Unix timestamp is a valid date format for Notification Service
- Both components work perfectly in isolation with their own test data

**The integration bug lives in the seam:**
- The contract between the two services doesn't specify the date format
- Each service made a different assumption about what "timestamp" means
- No integration test caught this because each service only tested with its own format

**Fix:** Define the contract explicitly - both services must agree on ISO 8601 or Unix timestamp. Update one service's implementation to match the other.
