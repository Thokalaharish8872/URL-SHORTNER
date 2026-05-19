# Module 5: Tickets - SkillSwap

## Ticket 1: Seed Database with Test Provider Data [AI-READY]

**Title:** Seed database with 3 test providers

**Context:** This ticket provides the seeded data required for Slice 1 (Browse and Book). Users need to see providers in the system to browse and book. This is a one-time seeding operation for development/demo purposes.

**Scope:** Create a database seed script that inserts 3 test providers with their services and time slots into the database. The script should be idempotent (can run multiple times without creating duplicates).

**Interface Contract:**
- Database schema (providers table):
  - id: UUID v4 (primary key)
  - name: string (max 100 chars)
  - category: string (max 50 chars)
  - rating: decimal (1-5 scale)
  - description: text
- Database schema (services table):
  - id: UUID v4 (primary key)
  - provider_id: UUID (foreign key to providers)
  - name: string (max 100 chars)
  - description: text
  - price: decimal
- Database schema (time_slots table):
  - id: UUID v4 (primary key)
  - service_id: UUID (foreign key to services)
  - start_time: timestamp
  - end_time: timestamp
  - status: enum ('available', 'booked')

**Acceptance Criteria:**
- Given an empty database
- When the seed script is executed
- Then 3 providers are inserted with unique UUIDs
- And each provider has exactly 1 service
- And each service has exactly 3 available time slots
- And running the script again does not create duplicate providers
- And time slots are set to future dates (not past dates)

**Constraints:**
- Use PostgreSQL (existing database connection)
- Use UUID v4 for all ID fields
- Follow existing project naming conventions (snake_case for columns)
- Seed data should be realistic (not "Provider 1", "Service A")

**Anti-scope:**
- No provider self-service interface (manual database seeding only)
- No provider images or photos
- No provider reviews or ratings (rating field seeded with default value)
- No real-time availability (time slots are static)
- No provider dashboard

---

## Ticket 2: GET /api/providers - List Providers [AI-READY]

**Title:** GET /api/providers - List providers with basic info

**Context:** This is the first API endpoint for Slice 1 (Browse and Book). Users need to see a list of providers to browse and select from. This endpoint is called by the frontend provider listing page.

**Scope:** Create a single GET endpoint at /api/providers that returns all providers with their basic information (name, category, rating). No pagination required for this ticket (assumes < 100 providers).

**Interface Contract:**
- Request: GET /api/providers
- Success response (200):
  ```json
  {
    "providers": [
      {
        "id": "uuid",
        "name": "string",
        "category": "string",
        "rating": "decimal"
      }
    ]
  }
  ```
- Error response (500):
  ```json
  {
    "error": "internal server error"
  }
  ```

**Acceptance Criteria:**
- Given the database has seeded provider data
- When a client sends GET /api/providers
- Then the endpoint returns HTTP 200
- And the response body contains a "providers" array
- And each provider has id, name, category, and rating fields
- And all providers in the database are returned
- And the response format matches the specified JSON structure
- And if the database is empty, returns an empty providers array (not 404)

**Constraints:**
- Use Express.js (existing framework in project)
- Use pg library for PostgreSQL queries (existing in project)
- Server runs on port 8080 (from environment variable PORT)
- Use existing PostgreSQL connection (connection string from DATABASE_URL env variable)
- Follow existing error response format (JSON with "error" field)
- No authentication required for this endpoint
- No pagination (return all providers)
- Apply rate limiting: 200 requests per minute per IP address
- Log provider list requests with request_id and timestamp
- Use global error handler for unexpected errors (returns 500 with generic message, no stack traces in production)
- Validate provider_id format in responses (must be valid UUID v4)

**Anti-scope:**
- No filtering by category
- No search functionality
- No sorting options
- No provider details (just basic info)
- No provider profile page endpoint (separate ticket)

---

## Ticket 3: GET /api/providers/:id - Get Provider Details

**Title:** GET /api/providers/:id - Get provider profile with services and slots

**Context:** After users see the provider list, they need to click on a provider to see their profile with services and available time slots. This is called by the frontend provider detail page.

**Scope:** Create a single GET endpoint at /api/providers/:id that returns a provider's profile including their services and available time slots.

**Interface Contract:**
- Request: GET /api/providers/:id
- Success response (200):
  ```json
  {
    "id": "uuid",
    "name": "string",
    "category": "string",
    "rating": "decimal",
    "description": "text",
    "services": [
      {
        "id": "uuid",
        "name": "string",
        "description": "text",
        "price": "decimal"
      }
    ],
    "available_slots": [
      {
        "id": "uuid",
        "start_time": "ISO 8601 timestamp",
        "end_time": "ISO 8601 timestamp"
      }
    ]
  }
  ```
- Error response (404):
  ```json
  {
    "error": "provider not found"
  }
  ```

**Acceptance Criteria:**
- Given a provider with ID exists in database
- When a client sends GET /api/providers/:id with valid UUID
- Then the endpoint returns HTTP 200
- And the response includes provider name, category, rating, description
- And the response includes the provider's services array
- And the response includes only available time slots (status = 'available')
- And time slots are returned in ISO 8601 format
- Given a non-existent provider ID
- When a client sends GET /api/providers/:id
- Then the endpoint returns HTTP 404
- And the error response is JSON with "error" field

**Constraints:**
- Use Express.js
- Use existing PostgreSQL connection (pg library)
- Follow existing error response format (JSON with "error" field)
- No authentication required
- Validate that :id is a valid UUID format
- Apply rate limiting: 200 requests per minute per IP address
- Log provider detail requests with provider_id, request_id, and timestamp
- Use global error handler for unexpected errors (returns 500 with generic message, no stack traces in production)
- Validate time slots are in the future (reject past dates with 400)

**Anti-scope:**
- No provider editing or updating
- No provider deletion
- No booking creation (separate ticket)
- No booked slots in the response (only available)
- No provider reviews or ratings display

---

## Ticket 4: POST /api/bookings - Create a Booking [AI-READY]

**Title:** POST /api/bookings - Create a new booking

**Context:** This is the core transaction in Slice 1. After selecting a provider and time slot, users click "Book" to create a booking. This endpoint is called by the frontend booking confirmation page.

**Scope:** Create a single POST endpoint at /api/bookings that creates a booking record and returns the booking confirmation.

**Interface Contract:**
- Request: POST /api/bookings
  ```json
  {
    "provider_id": "uuid",
    "service_id": "uuid",
    "slot_id": "uuid"
  }
  ```
- Success response (201):
  ```json
  {
    "booking_id": "uuid",
    "provider_id": "uuid",
    "service_id": "uuid",
    "slot_id": "uuid",
    "status": "confirmed",
    "created_at": "ISO 8601 timestamp"
  }
  ```
- Error responses:
  - 400: Invalid or missing required fields
    ```json
    {
      "error": "provider_id is required"
    }
    ```
  - 404: Provider, service, or slot not found
    ```json
    {
      "error": "provider not found"
    }
    ```
  - 409: Slot already booked
    ```json
    {
      "error": "slot unavailable"
    }
    ```

**Acceptance Criteria:**
- Given a valid provider_id, service_id, and slot_id that exist in database
- And the slot status is 'available'
- When a client sends POST /api/bookings with valid JSON body
- Then the endpoint returns HTTP 201
- And a booking record is created in the database
- And the booking status is 'confirmed'
- And the time slot status is updated to 'booked'
- And the response includes booking_id (UUID v4)
- Given missing provider_id in request body
- When a client sends POST /api/bookings
- Then the endpoint returns HTTP 400
- And the error message specifies which field is missing
- Given a non-existent slot_id
- When a client sends POST /api/bookings
- Then the endpoint returns HTTP 404
- Given a slot that is already booked
- When a client sends POST /api/bookings
- Then the endpoint returns HTTP 409
- And no booking record is created
- And the slot status remains 'booked'

**Constraints:**
- Use Express.js
- Use existing PostgreSQL connection (pg library)
- Follow existing error response format (JSON with "error" field)
- Use database transaction (booking creation + slot update must be atomic)
- No authentication required for this ticket (auth is separate)
- No payment processing (separate ticket)
- Apply rate limiting: 100 requests per minute per IP address
- Log booking creation with request_id, provider_id, slot_id, and timestamp
- Use global error handler for unexpected errors (returns 500 with generic message, no stack traces in production)
- Sanitize all input fields to prevent SQL injection (use parameterized queries)
- Booking creation is idempotent: if duplicate booking_id received, return existing booking (do not create duplicate)

**Anti-scope:**
- No payment processing
- No email confirmation
- No cancellation logic
- No booking modification
- No user association (user_id not stored, anonymous booking)
- No provider notification

---

## Ticket 5: POST /api/auth/register - User Registration

**Title:** POST /api/auth/register - Register a new user

**Context:** This is the first ticket for Slice 2 (User Authentication). Users need to create accounts before they can view their bookings. This is called by the frontend registration form.

**Scope:** Create a single POST endpoint at /api/auth/register that creates a new user account with email and password.

**Interface Contract:**
- Request: POST /api/auth/register
  ```json
  {
    "email": "string (valid email format)",
    "password": "string (min 8 chars)"
  }
  ```
- Success response (201):
  ```json
  {
    "user_id": "uuid",
    "email": "string",
    "created_at": "ISO 8601 timestamp"
  }
  ```
- Error responses:
  - 400: Invalid email format or password too short
    ```json
    {
      "error": "invalid email format"
    }
    ```
  - 409: Email already registered
    ```json
    {
      "error": "email already exists"
    }
    ```

**Acceptance Criteria:**
- Given a valid email and password (8+ chars)
- When a client sends POST /api/auth/register
- Then the endpoint returns HTTP 201
- And a user record is created in the database
- And the password is hashed (not stored in plaintext)
- And the response includes user_id and email
- Given an invalid email format
- When a client sends POST /api/auth/register
- Then the endpoint returns HTTP 400
- Given an email that already exists
- When a client sends POST /api/auth/register
- Then the endpoint returns HTTP 409
- And no new user is created

**Constraints:**
- Use Express.js
- Use existing PostgreSQL connection (pg library)
- Use bcrypt for password hashing (salt rounds: 10)
- Follow existing error response format (JSON with "error" field)
- Validate email format using regex
- No email verification (separate ticket)
- Apply rate limiting: 10 requests per minute per IP address (stricter for auth)
- Log registration attempts with email, request_id, and timestamp (do not log password)
- Use global error handler for unexpected errors (returns 500 with generic message, no stack traces in production)
- Validate password strength: min 8 chars, at least one letter and one number

**Anti-scope:**
- No social login (Google, Facebook)
- No password reset flow
- No email verification
- No profile editing
- No login endpoint (separate ticket)
- No session management

---

## Ticket 6: POST /api/auth/login - User Login

**Title:** POST /api/auth/login - Authenticate a user

**Context:** After registration, users need to log in to access their bookings. This is called by the frontend login form.

**Scope:** Create a single POST endpoint at /api/auth/login that authenticates a user with email and password and returns a session token.

**Interface Contract:**
- Request: POST /api/auth/login
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- Success response (200):
  ```json
  {
    "user_id": "uuid",
    "email": "string",
    "token": "string (JWT)"
  }
  ```
- Error responses:
  - 401: Invalid credentials
    ```json
    {
      "error": "invalid credentials"
    }
    ```
  - 404: User not found
    ```json
    {
      "error": "user not found"
    }
    ```

**Acceptance Criteria:**
- Given a user exists with the provided email
- And the password matches the hashed password
- When a client sends POST /api/auth/login
- Then the endpoint returns HTTP 200
- And the response includes user_id, email, and JWT token
- And the JWT token expires in 24 hours
- Given an invalid password
- When a client sends POST /api/auth/login
- Then the endpoint returns HTTP 401
- Given a non-existent email
- When a client sends POST /api/auth/login
- Then the endpoint returns HTTP 404

**Constraints:**
- Use Express.js
- Use existing PostgreSQL connection (pg library)
- Use bcrypt for password verification
- Use JWT for session tokens (secret key from JWT_SECRET env variable)
- Token expiration: 24 hours
- Follow existing error response format (JSON with "error" field)
- Apply rate limiting: 10 requests per minute per IP address (stricter for auth)
- Log login attempts with email, request_id, timestamp, and success/failure status (do not log password)
- Use global error handler for unexpected errors (returns 500 with generic message, no stack traces in production)
- Use constant-time comparison for password verification to prevent timing attacks

**Anti-scope:**
- No refresh tokens
- No social login
- No two-factor authentication
- No password reset
- No logout endpoint (stateless JWT)
- No role-based access control
