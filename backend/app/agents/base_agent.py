# backend/app/agents/base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):

    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

    @abstractmethod
    async def run(self):
        pass