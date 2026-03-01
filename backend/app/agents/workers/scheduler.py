# backend/app/agents/workers/scheduler.py

from celery.schedules import crontab
from app.agents.workers.celery_app import celery
from app.agents.workers.tasks import run_crew_for_user


# Example: run daily at 9 AM
celery.conf.beat_schedule = {
    "daily-life-review": {
        "task": "app.agents.workers.tasks.run_crew_for_user",
        "schedule": crontab(hour=9, minute=0),
        "args": (1,),  # Example user_id (later replace with dynamic user iteration)
    },
}

celery.conf.timezone = "UTC"