from crewai import Crew
from app.agents.crew.agents import create_agents
from app.agents.crew.tasks import create_tasks
from app.agents.context_builder import ContextBuilder


class CrewManager:

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

    async def run(self):

        context_builder = ContextBuilder(self.db, self.user_id)
        context = await context_builder.build("life overview")

        analyst, planner, executor = create_agents()
        t1, t2, t3 = create_tasks(context)

        crew = Crew(
            agents=[analyst, planner, executor],
            tasks=[t1, t2, t3],
            verbose=True
        )

        result = crew.kickoff()

        return result