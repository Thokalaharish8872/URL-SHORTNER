# URL Shortener Design Document

## Problem Statement
We need a URL shortening service that converts long URLs into short, shareable links. Users paste a long URL, receive a short code (e.g., `https://shrt.ly/abc123`), and the short code redirects to the original long URL when accessed.

## Requirements
- Generate unique short codes for any input URL
- Redirect short codes to original URLs
- Handle high traffic (millions of requests/day)
- Optional: Custom short codes, expiration dates, analytics

## Architecture

### Components
1. **API Service** - Accepts URL shortening requests and redirections
2. **Database** - Stores mapping between short codes and long URLs
3. **Cache** - Caches frequently accessed short codes for performance

### Data Model
```
ShortCode {
  id: string (primary key)
  short_code: string (unique, indexed)
  long_url: string
  created_at: timestamp
  expires_at: timestamp (optional)
}
```

### API Endpoints
- `POST /shorten` - Create short code from long URL
- `GET /:code` - Redirect to long URL
- `GET /info/:code` - Get metadata about short code

## Technology Stack
- API: Python (FastAPI) or Node.js (Express)
- Database: PostgreSQL (for persistence) or Redis (for simple key-value)
- Cache: Redis (for fast lookups)

## Scalability Considerations
- Use database sharding if write volume is high
- Use read replicas for redirect traffic
- Implement rate limiting to prevent abuse
- Consider CDN for global distribution
