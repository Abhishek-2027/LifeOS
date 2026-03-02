from celery import Celery
from app.core.config import settings

# Create Celery instance
celery = Celery(
    "lifeos",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Celery Configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,

    # Production-safe defaults
    task_time_limit=300,          # Hard timeout (5 min)
    task_soft_time_limit=270,     # Soft timeout (4.5 min)
    worker_prefetch_multiplier=1, # Prevent task overload
    task_acks_late=True,          # Retry if worker crashes
)

# Auto-discover tasks inside workers package
celery.autodiscover_tasks(packages=["app.agents.workers"])