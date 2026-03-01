# backend/app/agents/scheduler_agent.py

from app.agents.base_agent import BaseAgent
from datetime import datetime
from app.agents.llm_config import get_llm


class SchedulerAgent(BaseAgent):

    async def run(self):

        today = datetime.now().strftime("%A")

        llm = get_llm()

        prompt = f"""
        Today is {today}.
        Based on user productivity patterns, suggest daily focus strategy.
        """

        response = llm.invoke(prompt)

        return {"SchedulerAgent": response.content}