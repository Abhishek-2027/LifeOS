# backend/app/main.py

from fastapi import FastAPI
from app.api.v1 import (
    auth,
    users,
    memory,
    reasoning,
    documents,
    emails,
    dashboard,
    agents
)

app = FastAPI(
    title="LifeOS SaaS API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(memory.router)
app.include_router(reasoning.router)
app.include_router(documents.router)
app.include_router(emails.router)
app.include_router(dashboard.router)
app.include_router(agents.router)