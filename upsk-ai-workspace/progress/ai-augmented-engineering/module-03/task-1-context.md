# Task 1 Context Bundle: Create Team Data Model and Migration

TASK: Create Team data model and database migration

SYSTEM CONTEXT: [attach system-context.md]

FILES TO READ (with reasons):
1. api/app/models.py
   Reason: Shows the model definition pattern (SQLAlchemy ORM, field types, relationships, __repr__ methods).
   If omitted: Agent would define the model in a different style or miss SQLAlchemy conventions.

2. api/alembic/versions/[latest migration]
   Reason: Shows the migration format (table creation, column types, foreign keys, upgrade/downgrade functions).
   If omitted: Agent would write migrations in a different format or skip upgrade/downgrade functions.

3. api/app/config.py
   Reason: Shows database configuration pattern using Pydantic settings.
   If omitted: Agent might not understand how database connection is configured.

FILES TO MODIFY:
- None (this task creates new files only)

EXPECTED OUTPUT:
- New model in api/app/models.py: Team class with SQLAlchemy ORM fields
- New migration in api/alembic/versions/: [timestamp]_create_teams.py with upgrade/downgrade functions
