# Module 6: Interface Contracts

## Contract 1: Database Schema <-> All Tickets

**Shared types:**
- provider_id: uuid (v4)
- service_id: uuid (v4)
- slot_id: uuid (v4)
- user_id: uuid (v4)
- booking_id: uuid (v4)
- datetime format: ISO 8601 (e.g., "2025-03-15T14:30:00Z")
- rating: decimal (1-5 scale, 1 decimal place)
- price: decimal (2 decimal places)

**Database schema (shared contract):**

Table: providers
- id: uuid (v4, primary key)
- name: varchar(100) NOT NULL
- category: varchar(50) NOT NULL
- rating: decimal(2,1) DEFAULT 5.0
- description: text
- created_at: timestamp with time zone DEFAULT NOW()

Table: services
- id: uuid (v4, primary key)
- provider_id: uuid (foreign key to providers.id)
- name: varchar(100) NOT NULL
- description: text
- price: decimal(10,2) NOT NULL
- created_at: timestamp with time zone DEFAULT NOW()

Table: time_slots
- id: uuid (v4, primary key)
- service_id: uuid (foreign key to services.id)
- start_time: timestamp with time zone NOT NULL
- end_time: timestamp with time zone NOT NULL
- status: varchar(20) DEFAULT 'available' (values: 'available', 'booked')
- created_at: timestamp with time zone DEFAULT NOW()

Table: bookings
- id: uuid (v4, primary key)
- provider_id: uuid (foreign key to providers.id)
- service_id: uuid (foreign key to services.id)
- slot_id: uuid (foreign key to time_slots.id)
- user_id: uuid (nullable, foreign key to users.id)
- status: varchar(20) DEFAULT 'confirmed' (values: 'confirmed', 'failed')
- created_at: timestamp with time zone DEFAULT NOW()

Table: users
- id: uuid (v4, primary key)
- email: varchar(255) UNIQUE NOT NULL
- password_hash: varchar(255) NOT NULL
- created_at: timestamp with time zone DEFAULT NOW()

---

## Contract 2: Ticket 1 (Seed Database) <-> Ticket 2 (GET /api/providers)

**Seed Database provides:**
- Inserts 3 providers with valid UUIDs into providers table
- Each provider has exactly 1 service with valid UUID
- Each service has exactly 3 time slots with valid UUIDs and status='available'
- Time slots have future dates (not past)

**GET /api/providers consumes:**
- Reads from providers table
- Expects provider_id format: uuid (v4)
- Expects rating format: decimal(2,1)
- Returns provider data in specified JSON shape

**Contract:**
- Seed script must use UUID v4 for all IDs
- Seed script must set rating as decimal between 1.0 and 5.0
- Seed script must create time_slots with start_time > NOW()
- API endpoint must validate that provider_id is valid UUID before query
- API endpoint must handle empty result set gracefully (returns empty array, not 404)

---

## Contract 3: Ticket 2 (GET /api/providers) <-> Ticket 3 (GET /api/providers/:id)

**GET /api/providers provides:**
- GET /api/providers returns array of provider objects with id, name, category, rating

**GET /api/providers/:id consumes:**
- Accepts provider_id from the list returned by GET /api/providers
- Uses same provider_id format (uuid v4)

**Contract:**
- Both endpoints return provider_id in same format (uuid v4 string)
- Both endpoints return rating in same format (decimal, 1 decimal place)
- GET /api/providers/:id accepts the exact provider_id values returned by GET /api/providers
- If provider_id from GET /api/providers list does not exist in GET /api/providers/:id, this is a contract violation

---

## Contract 4: Ticket 1 (Seed Database) <-> Ticket 4 (POST /api/bookings)

**Seed Database provides:**
- Creates time_slots with status='available'
- Creates services with pricing

**POST /api/bookings consumes:**
- Accepts provider_id, service_id, slot_id that must exist
- Updates time_slots.status to 'booked' on successful booking

**Contract:**
- Seed script creates slot_id values that POST /api/bookings can consume
- POST /api/bookings must validate slot exists and status='available' before booking
- POST /api/bookings must update time_slots.status to 'booked' in same transaction as booking creation
- POST /api/bookings must use atomic transaction (booking creation + slot update)

---

## Contract 5: Ticket 4 (POST /api/bookings) <-> Future Tickets

**POST /api/bookings provides:**
- Returns booking_id (uuid v4)
- Creates booking record with provider_id, service_id, slot_id, status='confirmed'

**Future tickets (My Bookings, Notifications) will consume:**
- Read bookings table by user_id
- Use booking_id to reference specific bookings

**Contract:**
- booking_id is uuid v4 format
- booking status is one of: 'confirmed', 'failed'
- created_at is ISO 8601 timestamp
- Future tickets must handle case where booking has no user_id (anonymous booking from Slice 1)

---

## Contract 6: Ticket 5 (POST /api/auth/register) <-> Ticket 6 (POST /api/auth/login)

**POST /api/auth/register provides:**
- Creates user record with email and password_hash
- Returns user_id (uuid v4)

**POST /api/auth/login consumes:**
- Accepts email and password
- Verifies password against stored password_hash
- Returns user_id matching the registered user

**Contract:**
- Both tickets use bcrypt for password hashing/verification
- Both tickets use same password strength rules (min 8 chars, 1 letter, 1 number)
- Both tickets use same email validation regex
- Both tickets return user_id in same format (uuid v4)
- Login must verify password using bcrypt.compare() with same salt rounds as registration (10)
- Registration stores password_hash, login never stores password

---

## Contract 7: Ticket 6 (POST /api/auth/login) <-> Future Tickets (Authenticated Endpoints)

**POST /api/auth/login provides:**
- Returns JWT token with user_id encoded
- Token expires in 24 hours

**Future tickets (My Bookings, etc.) will consume:**
- Validate JWT token from Authorization header
- Extract user_id from token

**Contract:**
- JWT secret key from JWT_SECRET environment variable
- Token payload includes user_id (uuid v4)
- Token expiration: 24 hours from creation
- Token format: Bearer <token> in Authorization header
- Future tickets must validate token signature and expiration before processing
- Future tickets must extract user_id from token and use it for authorization
