# backend/app/agents/agent_manager.py

from app.agents.document_agent import DocumentAgent
from app.agents.email_agent import EmailAgent
from app.agents.scheduler_agent import SchedulerAgent
from app.agents.monitoring_agent import MonitoringAgent


class AgentManager:

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

    async def run_all(self):

        agents = [
            DocumentAgent(self.db, self.user_id),
            EmailAgent(self.db, self.user_id),
            SchedulerAgent(self.db, self.user_id),
            MonitoringAgent(self.db, self.user_id),
        ]

        results = {}

        for agent in agents:
            output = await agent.run()
            results.update(output)

        return results