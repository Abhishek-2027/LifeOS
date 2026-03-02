"""High‑level orchestrator for a CrewAI workflow.  The class is
importable even if ``crewai`` isn’t installed; methods will raise a
clear error if attempted to run without the library.
"""

from app.agents.context_builder import ContextBuilder

try:
    from crewai import Crew  # type: ignore[import]
    _CREWAI_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Crew = None
    _CREWAI_AVAILABLE = False

from app.agents.crew.agents import create_agents
from app.agents.crew.tasks import create_tasks


class CrewManager:

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

    async def run(self):

        context_builder = ContextBuilder(self.db, self.user_id)
        context = await context_builder.build("life overview")

        if not _CREWAI_AVAILABLE:
            raise ImportError("crewai is not installed; cannot run CrewManager")

        analyst, planner, executor = create_agents()
        t1, t2, t3 = create_tasks(context)

        crew = Crew(
            agents=[analyst, planner, executor],
            tasks=[t1, t2, t3],
            verbose=True
        )

        result = crew.kickoff()

        return result