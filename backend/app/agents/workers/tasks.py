# backend/app/agents/workers/tasks.py

import asyncio
from app.agents.crew.crew_manager import CrewManager
from app.core.database import AsyncSessionLocal
from app.agents.workers.celery_app import celery


@celery.task(bind=True)
def run_crew_for_user(self, user_id: int):
    """
    Run collaborative agent crew for a user asynchronously.
    """

    async def _run():
        async with AsyncSessionLocal() as db:
            manager = CrewManager(db=db, user_id=user_id)
            await manager.run()

    asyncio.run(_run())

    return f"Crew executed for user {user_id}"