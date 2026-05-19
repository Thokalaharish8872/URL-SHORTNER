# First 3 Prompts for Task Tree

## Prompt 1: Create Team Data Model and Migration

Create a Team data model and database migration for the project management API at `api/app/models.py`.

The Team model should have these exact fields:
- id: UUID, primary key, default=uuid4()
- name: String, required, maximum 100 characters
- description: String, optional, maximum 500 characters, nullable
- owner_id: UUID, foreign key to users.id, required
- created_at: DateTime, default=datetime.utcnow()
- updated_at: DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()

Follow these conventions from the existing User model in `api/app/models.py`:
- Use SQLAlchemy ORM with declarative_base
- Import UUID and datetime from standard library
- Use the same table naming convention (lowercase, plural)
- Include __repr__ method for debugging
- Use ForeignKey for relationships

Create an Alembic migration file in `api/alembic/versions/` that:
- Creates a teams table with the above columns
- Adds id as primary key with UUID type
- Makes name a VARCHAR(100) NOT NULL
- Makes description a VARCHAR(500) NULLABLE
- Adds owner_id as UUID NOT NULL with foreign key constraint to users.id
- Adds created_at and updated_at as TIMESTAMP
- Follows the migration pattern from existing migrations in `api/alembic/versions/`

Do not add any fields beyond those listed. Do not install new packages. Do not modify existing models or migrations.

## Prompt 2: Create TeamMembership Data Model and Migration

Create a TeamMembership data model and database migration for the project management API at `api/app/models.py`.

The TeamMembership model should have these exact fields:
- id: UUID, primary key, default=uuid4()
- team_id: UUID, foreign key to teams.id, nullable=False
- user_id: UUID, foreign key to users.id, nullable=False
- role: Enum with values 'admin', 'member', 'viewer', default='member'
- joined_at: DateTime, default=datetime.utcnow()

Follow these conventions:
- Use SQLAlchemy ORM with declarative_base from `api/app/models.py`
- Import the Team and User models you created in previous tasks
- Define the role enum using SQLAlchemy Enum type
- Add foreign key constraints to team_id and user_id
- Include __repr__ method for debugging

Create an Alembic migration file in `api/alembic/versions/` that:
- Creates a team_memberships table with the above columns
- Adds foreign key constraints: team_id references teams(id), user_id references users(id)
- Makes team_id and user_id NOT NULL
- Adds role as VARCHAR(20) with default 'member'
- Adds joined_at as TIMESTAMP
- Follows the migration pattern from existing migrations in `api/alembic/versions/`

Do not add any fields beyond those listed. Do not install new packages. Do not modify existing models or migrations.

## Prompt 3: Create Team CRUD API Endpoints

Create team CRUD API endpoints for the project management API at `api/app/main.py`.

First, create Pydantic schemas in `api/app/schemas.py`:
- TeamCreate: with fields name (str, required, max_length=100), description (str, optional, max_length=500)
- TeamResponse: with fields id (UUID), name (str), description (str | None), created_at (datetime), updated_at (datetime)

Follow the schema pattern from existing schemas in `api/app/schemas.py`.

Then, create these API endpoints in `api/app/main.py`:
- POST /teams: Create a new team. Accepts TeamCreate schema, returns TeamResponse with status 201. Validate name is required and max 100 chars. Validate description max 500 chars.
- GET /teams/{id}: Get a team by ID. Returns TeamResponse with status 200, or 404 if team not found.
- GET /teams: List all teams. Returns list of TeamResponse with status 200.
- PUT /teams/{id}: Update a team by ID. Accepts TeamCreate schema, returns TeamResponse with status 200, or 404 if team not found.
- DELETE /teams/{id}: Delete a team by ID. Returns status 204, or 404 if team not found.

Follow the API pattern from existing endpoints in `api/app/main.py`:
- Use FastAPI dependency injection for database session
- Use the same error handling pattern
- Include proper HTTP status codes
- Use Pydantic for request/response validation

Create a TeamService class in `api/app/services.py` with these methods:
- create_team(db, team_data): Create and return a new team
- get_team(db, team_id): Get team by ID or None
- list_teams(db): List all teams
- update_team(db, team_id, team_data): Update and return team
- delete_team(db, team_id): Delete team

Follow the service pattern from existing services in `api/app/services.py`.

Do not add any fields beyond those in the schemas. Do not modify existing endpoints. Do not install new packages.
