# backend/app/agents/email_agent.py

from app.agents.base_agent import BaseAgent
from app.services.email_service import EmailService
from app.agents.llm_config import get_llm
from app.agents.tools import get_tools

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


class EmailAgent(BaseAgent):

    async def run(self):

        emails = await EmailService.get_unprocessed(self.db, self.user_id)

        if not emails:
            return {"EmailAgent": "No new emails"}

        email_text = "\n".join([e.snippet for e in emails])

        llm = get_llm()
        tools = get_tools()

        # Create modern LangGraph ReAct agent
        agent = create_react_agent(
            model=llm,
            tools=tools
        )

        prompt = f"""
You are an intelligent email assistant.

Analyze the following emails:

{email_text}

Decide what actions should be taken.
"""

        # Invoke agent
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=prompt)]}
        )

        output = result["messages"][-1].content

        return {"EmailAgent": output}