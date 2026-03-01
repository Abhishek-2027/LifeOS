# backend/app/agents/monitoring_agent.py

from app.agents.base_agent import BaseAgent
from app.services.analytics_service import AnalyticsService
from app.agents.llm_config import get_llm


class MonitoringAgent(BaseAgent):

    async def run(self):

        memory_count = await AnalyticsService.memory_count(self.db, self.user_id)

        llm = get_llm()

        prompt = f"""
        User has {memory_count} memories stored.
        Analyze behavioral patterns and suggest improvements.
        """

        response = llm.invoke(prompt)

        return {"MonitoringAgent": response.content}