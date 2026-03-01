# backend/app/agents/workers/celery_app.py

from celery import Celery
from app.core.config import settings

celery = Celery(
    "lifeos",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Auto-discover tasks
celery.autodiscover_tasks(["app.agents.workers"])