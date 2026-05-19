# Task 3 Context Bundle: Create Team CRUD API Endpoints

TASK: Create team CRUD API endpoints

SYSTEM CONTEXT: [attach system-context.md]

FILES TO READ (with reasons):
1. api/app/main.py
   Reason: Shows route registration pattern using FastAPI decorators, dependency injection for database session, error handling with HTTPException.
   If omitted: Agent would register routes differently or miss dependency injection pattern.

2. api/app/models.py
   Reason: Shows Team model definition and database session pattern. Endpoints need to interact with this model.
   If omitted: Agent might not understand how to query or create Team objects.

3. api/app/schemas.py
   Reason: Shows Pydantic schema pattern for request/response validation. Need to create TeamCreate and TeamResponse schemas.
   If omitted: Agent would create schemas in different style or miss validation patterns.

4. api/app/services.py
   Reason: Shows service class pattern for business logic. Need to create TeamService.
   If omitted: Agent might put business logic directly in route handlers instead of service layer.

5. system-context.md (Error Handling section)
   Reason: Contains concrete example of HTTPException usage for error responses.
   If omitted: Agent might invent different error format like {status: 'error', message: '...', statusCode: 400} instead of required {detail: 'message'} format.

FILES TO MODIFY:
- api/app/main.py (to add new route handlers)
- api/app/schemas.py (to add TeamCreate and TeamResponse schemas)
- api/app/services.py (to add TeamService class)

EXPECTED OUTPUT:
- New schemas in api/app/schemas.py: TeamCreate, TeamResponse
- New service in api/app/services.py: TeamService with CRUD methods
- New routes in api/app/main.py: POST /teams, GET /teams/{id}, GET /teams, PUT /teams/{id}, DELETE /teams/{id}
