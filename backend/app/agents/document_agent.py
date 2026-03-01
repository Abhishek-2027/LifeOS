# backend/app/agents/document_agent.py

from app.agents.base_agent import BaseAgent
from app.agents.context_builder import ContextBuilder
from app.agents.llm_config import get_llm
from app.agents.tools import get_tools
from app.agents.memory_sync import MemorySync

from langchain.agents import initialize_agent, AgentType


class DocumentAgent(BaseAgent):

    async def run(self):

        context_builder = ContextBuilder(self.db, self.user_id)
        context = await context_builder.build("documents and tasks")

        llm = get_llm()
        tools = get_tools()

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

        prompt = f"""
        You are a cognitive assistant.
        Based on this user memory context:
        {context}

        Suggest document-related improvements or actions.
        """

        response = agent.run(prompt)

        sync = MemorySync()
        await sync.sync(self.db, self.user_id, response)

        return {"DocumentAgent": response}