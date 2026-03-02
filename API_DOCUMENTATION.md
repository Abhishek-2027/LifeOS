# LifeOS API Documentation

## Backend Status: ✅ OPERATIONAL

All core API endpoints are functional and tested. The backend is ready for frontend integration.

---

## Quick Start

### 1. Start Backend Server
```bash
cd c:\LifeOS\backend
python -m uvicorn app.main:app --reload
```
Server runs on: `http://127.0.0.1:8000`

### 2. View API Documentation
Open in browser: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Login User
```
POST /auth/login
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Memory Management

All memory endpoints require authentication header:
```
Authorization: Bearer <access_token>
```

#### Add Memory
```
POST /memory/add
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "text": "Had a meeting about project roadmap",
  "memory_type": "episodic",           # episodic | semantic
  "emotion": "positive",               # positive | negative | neutral
  "importance": 0.8                    # 0.0 to 1.0
}

Response (200):
{
  "id": 1,
  "user_id": 1,
  "text": "Had a meeting about project roadmap",
  "memory_type": "episodic",
  "emotion": "positive",
  "importance": 0.8,
  "meta_data": "{}",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Search Memories
```
GET /memory/search?query=meeting
Authorization: Bearer <token>

Response (200):
[
  {
    "id": 1,
    "text": "Had a meeting about project roadmap",
    "memory_type": "episodic",
    "emotion": "positive",
    "importance": 0.8,
    "similarity_score": 0.9
  }
]
```

#### Get All Memories
```
GET /memory/list
Authorization: Bearer <token>

Response (200):
[
  {
    "id": 1,
    "text": "Memory text...",
    "memory_type": "episodic",
    "emotion": "positive",
    "importance": 0.8,
    "timestamp": "2024-01-15T10:30:00"
  },
  ...
]
```

---

## Frontend Integration Example

### JavaScript/Fetch API

```javascript
const API_URL = 'http://127.0.0.1:8000';
let authToken = '';

// 1. Register
async function register(email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  authToken = data.access_token;
  return data;
}

// 2. Add Memory
async function addMemory(text, type, emotion, importance) {
  const response = await fetch(`${API_URL}/memory/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authToken}`
    },
    body: JSON.stringify({
      text,
      memory_type: type,
      emotion,
      importance
    })
  });
  return response.json();
}

// 3. Search Memories
async function searchMemory(query) {
  const response = await fetch(`${API_URL}/memory/search?query=${encodeURIComponent(query)}`, {
    headers: { 'Authorization': `Bearer ${authToken}` }
  });
  return response.json();
}

// Usage Example
async function main() {
  // Register user
  await register('user@example.com', 'password123');
  
  // Add some memories
  await addMemory('Had a great meeting today', 'episodic', 'positive', 0.8);
  await addMemory('Learned about new framework', 'semantic', 'positive', 0.7);
  
  // Search memories
  const results = await searchMemory('meeting');
  console.log(results);
}

main();
```

---

## Database Status

**Type**: SQLite (development)  
**Location**: `c:\LifeOS\backend\lifeos.db`  
**Size**: ~36.8 KB

Tables:
- `users` - User accounts & authentication
- `memories` - User memories with metadata
- `documents` - Document storage (schema ready)
- `emails` - Email records (schema ready)
- `agent_logs` - Agent activity logging

---

## Development Configuration

**Environment File**: `c:\LifeOS\backend\.env`

```
DATABASE_URL=sqlite+aiosqlite:///./lifeos.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OLLAMA_URL=http://localhost:11434
```

---

## Production Readiness

### To switch to PostgreSQL for production:

1. Update `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/lifeos
   ```

2. Install PostgreSQL and create database

3. Run migrations with Alembic (if available)

4. Rebuild with pgvector support for semantic search

---

## Error Handling

All endpoints return standard HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad Request (invalid data) |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Not Found |
| 500 | Server Error |

Error responses include a `detail` field explaining the issue.

---

## Testing

Run comprehensive test:
```bash
cd c:\LifeOS
python test_comprehensive.py
```

This tests:
- API health
- User registration
- User login
- Memory creation (5 records)
- Memory search (5 queries)
- OpenAPI schema

---

## Performance Notes

- **Memory Search**: Uses text-based substring matching (O(n))
- **Concurrent Users**: SQLite with StaticPool supports single concurrent connection
- **For Production**: Migrate to PostgreSQL with pgvector for semantic similarity

---

## Support

- API Docs: http://127.0.0.1:8000/docs
- OpenAPI Schema: http://127.0.0.1:8000/openapi.json
- Backend Code: c:\LifeOS\backend\app\*
