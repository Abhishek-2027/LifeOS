# backend/app/services/agent_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.agent_manager import AgentManager


class AgentService:

    @staticmethod
    async def run_agents(user_id: int, db: AsyncSession):

        manager = AgentManager(db=db, user_id=user_id)
        result = await manager.run_all()

        return result

    @staticmethod
    async def run_email_agent(user_id: int):
        return {"status": "Email agent started", "user_id": user_id}

    @staticmethod
    async def run_monitoring_agent(user_id: int):
        return {"status": "Monitoring agent started", "user_id": user_id}
