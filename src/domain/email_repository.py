# domain/email_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import EmailMessage

# Abstract base class for the email message repository.
# Defines the contract for storing and retrieving email data.
class EmailRepository(ABC):
    @abstractmethod
    def add_email(self, email: EmailMessage) -> None:
        """Adds a new email message to the repository."""
        pass

    @abstractmethod
    def get_emails_to_send(self, limit: int) -> List[EmailMessage]:
        """Retrieves a limited number of unsent emails."""
        pass

    @abstractmethod
    def update_email_status(self, email_id: int, is_sent: bool) -> None:
        """Updates the sent status of an email message."""
        pass
