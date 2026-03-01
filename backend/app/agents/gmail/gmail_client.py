import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GmailClient:

    def __init__(self, credentials_path="token.json"):
        creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build("gmail", "v1", credentials=creds)

    def fetch_unread(self):

        results = self.service.users().messages().list(
            userId="me",
            labelIds=["UNREAD"]
        ).execute()

        return results.get("messages", [])