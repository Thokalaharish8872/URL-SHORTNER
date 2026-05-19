# Module 5 Context: Ticket Writing

## Micro-Exercise: Questions for Vague Ticket (Version A)

**Ticket:** "Create booking endpoint. Build an API endpoint that lets users book a service provider. It should validate the input and return a confirmation. Handle errors appropriately."

**Questions before I could start coding:**

1. What HTTP method (GET, POST, PUT, DELETE)?
2. What URL path (/api/booking, /api/bookings, /v1/bookings, etc.)?
3. What fields are required in the request body?
4. What fields are optional in the request body?
5. What data types for each field (string, number, UUID)?
6. What does the success response look like?
7. What HTTP status code for success (200, 201, 204)?
8. What counts as invalid input that needs validation?
9. What HTTP status codes for errors (400, 404, 409, 500)?
10. What error response format (JSON with error field, message, code)?
11. Does this require authentication?
12. What database schema for bookings (table name, columns)?
13. What happens if the provider doesn't exist?
14. What happens if the time slot doesn't exist?
15. What happens if the slot is already booked?
16. Should this trigger any notifications?
17. Is payment processing part of this or separate?
18. Should the booking be confirmed immediately or pending?

**18 questions from 3 sentences.** Every question is a gap in the specification that would require a round-trip delay before work can begin.
