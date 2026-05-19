# Module 5 Fix: Data Recovery and Communication

## Database Backup Status
- Full DB backup: Daily at 06:00 UTC (last backup: 2024-03-15 06:00 UTC)
- WAL/binlog archiving: Enabled, continuous
- Point-in-time recovery (PITR): Available up to 5 minutes before current time
- The 12 deleted links existed as of 14:20:00 UTC (before attack window 14:22-14:32)

## Recovery Plan

### Step 1: Query PITR Backup
Query the point-in-time recovery backup at 14:20:00 UTC for the 12 deleted link IDs to extract full row data.

### Step 2: Extract Data
Extract the complete row data (code, long_url, created_by, created_at, etc.) for all 12 deleted links.

### Step 3: Re-insert Rows
Re-insert the 12 rows into the production database with their original data, preserving original IDs and timestamps.

### Step 4: Verify Restoration
Verify that all 12 links resolve correctly by testing each short code.

### Step 5: Notify Affected Users
Send notification to the 8 affected users explaining their links were temporarily unavailable but have been restored.

## Stakeholder Data-Loss Message

**To VP of Product**:

"Follow-up on the security incident: During the attack window, 12 short links belonging to 8 users were deleted by the attacker before we deployed the fix. We have restored all 12 links from our database backup using point-in-time recovery and verified they are working correctly. No data was permanently lost. We will be notifying the affected users and conducting a full postmortem to ensure this class of vulnerability cannot recur."

## Key Points

- **Point-in-time recovery**: Like a DVR for database - can query backup at specific timestamp to extract just the needed rows
- **No full restore needed**: Can extract specific rows without restoring entire database
- **Transparency is critical**: Must communicate data loss and recovery, even after saying incident was resolved
- **Verification essential**: Don't assume recovery worked - verify each restored link resolves correctly
- **User notification**: Affected users deserve to know what happened and that their data is restored
