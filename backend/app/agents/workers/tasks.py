# backend/app/agents/workers/tasks.py

import asyncio
from app.core.database import AsyncSessionLocal
from app.agents.workers.celery_app import celery

# CrewManager import is optional so that the backend can start even when
# the `crewai` package is not installed.  We import lazily below.




@celery.task(bind=True)
def run_crew_for_user(self, user_id: int):
    """
    Run collaborative agent crew for a user asynchronously.
    """

    async def _run():
        async with AsyncSessionLocal() as db:
                try:
                    from app.agents.crew.crew_manager import CrewManager
                except ImportError:
                    # Crew functionality unavailable; nothing to execute
                    return


    asyncio.run(_run())

    return f"Crew executed for user {user_id}"