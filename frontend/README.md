LifeOS Frontend Demo

This is a minimal static frontend demonstrating API integration for:
- Register (/auth/register)
- Login (/auth/login)
- Personal memory CRUD (add & search)
- Document upload (/documents/upload)
- Email synchronization and listing (/emails)
- Dashboard overview (/dashboard/overview)
- Agent triggers (email & monitoring)
- Reasoning queries (/reasoning/analyze)

The UI is intentionally lightweight but styled as a basic SaaS dashboard. It can be served
from a static web server or opened directly in the browser.

How to use:
1. Start backend (in c:\LifeOS\backend):
```
python -m uvicorn app.main:app --reload
```
2. Open `c:\LifeOS\frontend\index.html` in your browser (or serve with a static server).
3. Enter email/password, register or login, then add/search memories.

If your frontend runs on a different origin, add its origin to CORS allow_origins in `app/main.py`.
