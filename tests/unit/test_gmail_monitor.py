import pytest
from unittest.mock import MagicMock, patch
from src.skills.gmail_monitor import GmailMonitor, GmailAuthenticator
from src.models.email import EmailMessage

@pytest.fixture
def mock_authenticator():
    auth = MagicMock(spec=GmailAuthenticator)
    auth.get_credentials.return_value = MagicMock()
    return auth

@pytest.fixture
def monitor(mock_authenticator):
    with patch("src.skills.gmail_monitor.build") as mock_build:
        monitor = GmailMonitor(authenticator=mock_authenticator)
        return monitor

def test_filter_recruitment_emails_match(monitor):
    # Mock listing messages
    monitor.list_recent_messages = MagicMock(return_value=[{"id": "123"}])
    
    # Mock getting message details
    mock_email = EmailMessage(
        id="123",
        thread_id="thread1",
        subject="Interview Invitation",
        snippet="We would like to invite you for an interview.",
        sender="HR <hr@company.com>"
    )
    monitor.get_message_details = MagicMock(return_value=mock_email)
    
    results = monitor.filter_recruitment_emails(keywords=["Interview"])
    
    assert len(results) == 1
    assert results[0].subject == "Interview Invitation"

def test_filter_recruitment_emails_no_match(monitor):
    monitor.list_recent_messages = MagicMock(return_value=[{"id": "456"}])
    
    mock_email = EmailMessage(
        id="456",
        thread_id="thread2",
        subject="Weekly Newsletter",
        snippet="Here is your weekly update.",
        sender="News <news@generic.com>"
    )
    monitor.get_message_details = MagicMock(return_value=mock_email)
    
    results = monitor.filter_recruitment_emails(keywords=["Hired", "Offer"])
    
    assert len(results) == 0
