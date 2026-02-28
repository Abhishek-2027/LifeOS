# backend/app/api/v1/agents.py

from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run-email-agent")
async def run_email_agent(current_user=Depends(get_current_user)):
    return await AgentService.run_email_agent(current_user.id)


@router.post("/run-monitoring")
async def run_monitoring_agent(current_user=Depends(get_current_user)):
    return await AgentService.run_monitoring_agent(current_user.id)