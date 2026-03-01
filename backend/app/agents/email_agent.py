# backend/app/agents/email_agent.py

from app.agents.base_agent import BaseAgent
from app.services.email_service import EmailService
from app.agents.llm_config import get_llm
from app.agents.tools import get_tools
from langchain.agents import initialize_agent, AgentType


class EmailAgent(BaseAgent):

    async def run(self):

        emails = await EmailService.get_unprocessed(self.db, self.user_id)

        if not emails:
            return {"EmailAgent": "No new emails"}

        email_text = "\n".join([e.snippet for e in emails])

        llm = get_llm()
        tools = get_tools()

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

        prompt = f"""
        Analyze the following emails:
        {email_text}

        Decide what actions should be taken.
        """

        response = agent.run(prompt)

        return {"EmailAgent": response}