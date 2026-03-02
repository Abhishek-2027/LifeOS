# backend/app/agents/document_agent.py

from app.agents.base_agent import BaseAgent
from app.agents.context_builder import ContextBuilder
from app.agents.llm_config import get_llm
from app.agents.memory_sync import MemorySync

# stripping out `langchain_core`/`langgraph` imports to avoid
# dependency conflicts; we now call the LLM directly



class DocumentAgent(BaseAgent):

    async def run(self):

        # Build contextual memory
        context_builder = ContextBuilder(self.db, self.user_id)
        context = await context_builder.build("documents and tasks")

        llm = get_llm()

        prompt = f"""
You are a cognitive assistant that helps manage documents and tasks.

Based on this user memory context:

{context}

Suggest document-related improvements or actions.
"""

        # call the LLM directly
        output = llm.generate(prompt)

        # Sync memory
        sync = MemorySync()
        await sync.sync(self.db, self.user_id, output)

        return {"DocumentAgent": output}