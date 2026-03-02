# LifeOS Backend - Troubleshooting Guide

## Common Issues & Solutions

### Server Won't Start

#### Error: `ModuleNotFoundError: No module named 'app'`
**Cause**: Running uvicorn from wrong directory  
**Solution**:
```bash
# WRONG:
cd c:\LifeOS
python -m uvicorn app.main:app

# CORRECT:
cd c:\LifeOS\backend
python -m uvicorn app.main:app --reload
```

#### Error: `Connection refused` or no response on http://127.0.0.1:8000
**Cause**: Server not running  
**Solution**:
1. Check if terminal shows "Application startup complete"
2. Ensure you're in `c:\LifeOS\backend` directory
3. Check for error messages in terminal
4. Try: `python -m uvicorn app.main:app` (without --reload)

---

### Authentication Issues

#### Error: `401 Unauthorized` when accessing protected endpoints
**Cause**: Missing or invalid token  
**Solution**:
```javascript
// Add authorization header to request
fetch('/memory/add', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
```

#### Error: `Invalid token` or `Token expired`
**Cause**: Token malformed or expired (60 minutes)  
**Solution**:
1. Register again to get new token
2. Increase TOKEN_EXPIRE_MINUTES in `.env` (development only)
3. Token is valid for 60 minutes from generation

---

### Memory Endpoints

#### Error: `500` on `/memory/add`
**Cause**: Usually metadata or field type issue  
**Solution**:
1. Check request body has `text`, `memory_type`, `emotion`, `importance`
2. `memory_type` must be: `episodic` or `semantic`
3. `emotion` must be: `positive`, `negative`, or `neutral`
4. `importance` must be: number between 0.0 and 1.0

Correct request:
```json
{
  "text": "Memory content here",
  "memory_type": "episodic",
  "emotion": "positive",
  "importance": 0.8
}
```

#### Search returns no results
**Cause**: Text-based search is case-insensitive but requires word match  
**Solution**:
1. Search is substring matching: "python" finds "Python async"
2. Check spelling exactly as in memory text
3. Use single words for better results
4. Example working searches: "meeting", "python", "api", "feature"

Bad search: "great meeting roadmap" (looks for all three words in one memory)  
Good search: "meeting" (finds any memory with "meeting")

---

### Database Issues

#### Error: `database is locked` (SQLite)
**Cause**: Multiple processes accessing database simultaneously  
**Solution**:
1. Close other terminals/processes using database
2. Stop backend and restart: `Ctrl+C` then restart
3. For production: Migrate to PostgreSQL

#### Error: `sqlite3.OperationalError: no such table`
**Cause**: Database hasn't been initialized  
**Solution**:
```bash
cd c:\LifeOS\backend
python

# In Python shell:
from app.core.database import Base, engine
import asyncio

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
```

---

### CORS Issues (Frontend)

#### Error: `No 'Access-Control-Allow-Origin' header`
**Cause**: Frontend on different origin than backend  
**Solution**:

Update [app/main.py](app/main.py):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

(already configured in current version)

---

### Ollama Integration

#### Error: `Connection refused` when calling LLM features
**Cause**: Ollama server not running  
**Solution**:
1. Install Ollama from https://ollama.ai
2. Open new terminal and run: `ollama serve`
3. In another terminal, pull a model: `ollama pull mistral`
4. Wait 5-10 minutes for download
5. Backend will auto-detect Ollama

#### LLM responses are slow or timeout
**Cause**: Model is large or system is resource-constrained  
**Solution**:
1. Use smaller model: `ollama pull phi` (faster)
2. Increase timeout in [app/reasoning_engine/llm_reasoner.py](app/reasoning_engine/llm_reasoner.py):
   ```python
   timeout=60  # Increase from 30 seconds
   ```

---

### Development Tools

#### Run Tests
```bash
cd c:\LifeOS
python test_comprehensive.py
```

Expected output: All PASS with 5 memories added

#### View API Documentation
1. Start server
2. Open: http://127.0.0.1:8000/docs
3. Try endpoints with Swagger UI

#### Check Database Contents
```bash
# From c:\LifeOS\backend
python

from app.core.database import SessionLocal
from app.models import User, Memory

async def check_db():
    async with SessionLocal() as db:
        users = await db.execute(select(User))
        print(f"Users: {len(users.scalars().all())}")
        
        memories = await db.execute(select(Memory))
        print(f"Memories: {len(memories.scalars().all())}")

asyncio.run(check_db())
```

---

### Performance Optimization

#### Memory Search is Slow
**Current**: O(n) substring search on all memories  
**Solution**:
1. For development: OK (small dataset)
2. For production: 
   - Migrate to PostgreSQL
   - Use pgvector extension
   - Implement embedding-based search

#### Database Queries are Slow
**Current**: SQLite with single connection  
**Solution**:
1. For development: Acceptable
2. For production:
   - Use PostgreSQL + asyncpg
   - Add database indexes
   - Cache frequently accessed data

---

### Frontend Integration Checklist

- [ ] Backend running on http://127.0.0.1:8000
- [ ] `test_comprehensive.py` passes
- [ ] Frontend configured to call API endpoints
- [ ] CORS allowed for frontend origin
- [ ] Frontend stores JWT token from `/auth/register`
- [ ] Frontend uses token in `Authorization: Bearer <token>` header
- [ ] Frontend sends all required fields to `/memory/add`
- [ ] Frontend handles 401 errors (expired token, re-register)
- [ ] API Docs visible at http://127.0.0.1:8000/docs

---

### Reset Database (Development Only)

If you need to start fresh:
```bash
cd c:\LifeOS\backend

# Remove old database
del lifeos.db

# Restart server to reinitialize
python -m uvicorn app.main:app --reload
```

---

### Debug Mode

Add debug prints to understand flow:

```python
# In app/services/memory_service.py
async def add_memory(self, user_id: int, memory: MemoryCreate):
    print(f"DEBUG: Adding memory for user {user_id}: {memory.text}")
    # ... rest of code
    print(f"DEBUG: Memory created with ID: {created_memory.id}")
```

Then watch terminal output while testing.

---

### Common Success Indicators

✅ Backend working:
- `curl http://127.0.0.1:8000` returns `{"status": "LifeOS backend running"}`
- API docs load at http://127.0.0.1:8000/docs
- Test script completes without errors

✅ Authentication working:
- Register endpoint returns token
- Token is valid JWT (decode at jwt.io)
- Protected endpoints return 401 without token

✅ Memory working:
- Add 3+ memories without errors
- Search finds results
- Results have correct text and emotion

---

### Still Having Issues?

1. **Check error message carefully** - it usually tells you the problem
2. **Look at server terminal** - error details often there
3. **Test endpoints with Swagger** - at http://127.0.0.1:8000/docs
4. **Enable debug logging** in [app/core/logging.py](app/core/logging.py)
5. **Run test script** to isolate issue

---

Last Updated: January 18, 2025
