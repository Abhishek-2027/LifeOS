# backend/app/agents/document_agent.py

from app.agents.base_agent import BaseAgent
from app.agents.context_builder import ContextBuilder
from app.agents.llm_config import get_llm
from app.agents.tools import get_tools
from app.agents.memory_sync import MemorySync

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


class DocumentAgent(BaseAgent):

    async def run(self):

        # Build contextual memory
        context_builder = ContextBuilder(self.db, self.user_id)
        context = await context_builder.build("documents and tasks")

        llm = get_llm()
        tools = get_tools()

        # Create modern LangGraph ReAct agent
        agent = create_react_agent(
            model=llm,
            tools=tools
        )

        prompt = f"""
You are a cognitive assistant that helps manage documents and tasks.

Based on this user memory context:

{context}

Suggest document-related improvements or actions.
"""

        # Invoke agent asynchronously
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=prompt)]}
        )

        # Get final model response
        output = result["messages"][-1].content

        # Sync memory
        sync = MemorySync()
        await sync.sync(self.db, self.user_id, output)

        return {"DocumentAgent": output}