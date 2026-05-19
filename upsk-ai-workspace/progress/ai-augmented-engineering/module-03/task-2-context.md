# Task 2 Context Bundle: Create TeamMembership Data Model and Migration

TASK: Create TeamMembership data model and database migration

SYSTEM CONTEXT: [attach system-context.md]

FILES TO READ (with reasons):
1. api/app/models.py
   Reason: Shows the model definition pattern and now includes Team model from Task 1. TeamMembership needs foreign key to Team.
   If omitted: Agent might define foreign key relationship incorrectly or use wrong field names.

2. api/alembic/versions/[latest migration]
   Reason: Shows the migration format including foreign key constraints.
   If omitted: Agent might miss foreign key constraint syntax or create table without proper relationships.

3. api/app/models.py (User model section)
   Reason: TeamMembership needs foreign key to User. Shows how User model is defined.
   If omitted: Agent might use wrong field name for user relationship.

FILES TO MODIFY:
- api/app/models.py (to add TeamMembership model)

EXPECTED OUTPUT:
- New model in api/app/models.py: TeamMembership class with SQLAlchemy ORM fields
- New migration in api/alembic/versions/: [timestamp]_create_team_memberships.py with foreign key constraints
