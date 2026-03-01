from app.agents.base_agent import BaseAgent
from app.agents.gmail.gmail_client import GmailClient
from app.services.email_service import EmailService
from app.schemas.email_schema import EmailCreate


class GmailAgent(BaseAgent):

    async def run(self):

        client = GmailClient()
        messages = client.fetch_unread()

        for msg in messages:
            await EmailService.add_email(
                self.db,
                self.user_id,
                EmailCreate(
                    subject="New Email",
                    sender="Gmail",
                    snippet="Fetched from Gmail API"
                )
            )

        return {"GmailAgent": f"{len(messages)} emails fetched"}