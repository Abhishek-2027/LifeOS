# backend/app/agents/email_agent.py

from app.agents.base_agent import BaseAgent
from app.services.email_service import EmailService
from app.agents.llm_config import get_llm

# previously used langchain/langgraph; those imports were causing
# version conflicts and are no longer required.



class EmailAgent(BaseAgent):

    async def run(self):

        emails = await EmailService.get_unprocessed(self.db, self.user_id)

        if not emails:
            return {"EmailAgent": "No new emails"}

        email_text = "\n".join([e.snippet for e in emails])

        llm = get_llm()

        prompt = f"""
You are an intelligent email assistant.

Analyze the following emails:

{email_text}

Decide what actions should be taken.
"""

        # simple generate call rather than using an external agent framework
        output = llm.generate(prompt)

        return {"EmailAgent": output}