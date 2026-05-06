import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional

from src.models.email import EmailMessage
from src.utils.logger import logger

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailAuthenticator:
    """Handles Google OAuth2 authentication flow."""
    
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path

    def get_credentials(self) -> Credentials:
        """Gets valid user credentials from storage or runs OAuth flow."""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing Gmail API token...")
                creds.refresh(Request())
            else:
                logger.info("Initializing new Gmail API OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        
        return creds

class GmailMonitor:
    """Monitors Gmail inbox for recruitment-related emails."""
    
    def __init__(self, authenticator: Optional[GmailAuthenticator] = None):
        self.authenticator = authenticator or GmailAuthenticator()
        self.service = None

    def _get_service(self):
        """Lazy initialization of the Gmail API service."""
        if not self.service:
            creds = self.authenticator.get_credentials()
            self.service = build("gmail", "v1", credentials=creds)
        return self.service

    def list_recent_messages(self, max_results: int = 50) -> List[dict]:
        """Fetches a list of recent message summaries."""
        try:
            service = self._get_service()
            results = service.users().messages().list(userId="me", maxResults=max_results).execute()
            return results.get("messages", [])
        except HttpError as error:
            logger.error(f"An error occurred while listing messages: {error}")
            return []

    def get_message_details(self, message_id: str) -> Optional[EmailMessage]:
        """Fetches full details for a specific message ID."""
        try:
            service = self._get_service()
            msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
            
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown Sender")
            
            return EmailMessage(
                id=msg["id"],
                thread_id=msg["threadId"],
                subject=subject,
                snippet=msg.get("snippet", ""),
                sender=sender,
                labels=msg.get("labelIds", [])
            )
        except HttpError as error:
            logger.error(f"An error occurred while fetching message {message_id}: {error}")
            return None

    def filter_recruitment_emails(self, keywords: List[str] = ["Hired", "Interview", "Offer"]) -> List[EmailMessage]:
        """Filters recent emails for recruitment keywords."""
        logger.info(f"Scanning inbox for keywords: {keywords}")
        recent_summaries = self.list_recent_messages()
        filtered_emails = []

        for summary in recent_summaries:
            email = self.get_message_details(summary["id"])
            if email:
                # Check subject and snippet for keywords (case-insensitive)
                content = (email.subject + " " + email.snippet).lower()
                if any(kw.lower() in content for kw in keywords):
                    logger.info(f"Found recruitment email: {email.subject}")
                    filtered_emails.append(email)
        
        return filtered_emails

if __name__ == "__main__":
    # Quick manual test
    monitor = GmailMonitor()
    results = monitor.filter_recruitment_emails()
    print(f"\nFound {len(results)} recruitment-related emails:")
    for res in results:
        print(f"- [{res.subject}] from {res.sender}")
