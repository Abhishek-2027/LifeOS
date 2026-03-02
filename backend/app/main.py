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
from app.core.database import engine
from app.models.base import Base

# Import all models to register them with SQLAlchemy
from app.models import (  # noqa: F401
    User,
    Memory,
    Document,
    Email,
    AgentLog,
)

app = FastAPI(
    title="LifeOS SaaS API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    """Application startup - tables should be created by migrations"""
    print("LifeOS backend is starting...")

@app.get("/")
async def root():
    return {"status": "LifeOS backend running"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(memory.router)
app.include_router(reasoning.router)
app.include_router(documents.router)
app.include_router(emails.router)
app.include_router(dashboard.router)
app.include_router(agents.router)