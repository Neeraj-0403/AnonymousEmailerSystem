# application/email_service.py

from domain.email_repository import EmailRepository
from domain.models import EmailMessage
from infrastructure.ai_service import AIService
from infrastructure.logger import logger

class EmailService:
    """
    Application service for handling email-related use cases.
    It combines AI moderation, encryption, and queuing logic.
    """
    def __init__(self, email_repository: EmailRepository, ai_service: AIService):
        self.email_repository = email_repository
        self.ai_service = ai_service

    def queue_email_for_sending(self, recipient: str, subject: str, content: str) -> bool:
        """
        Validates email content with AI and queues the email for asynchronous sending.
        
        Args:
            recipient (str): The email recipient.
            subject (str): The email subject.
            content (str): The email content.
            
        Returns:
            bool: True if the email was successfully queued, False otherwise.
        """
        try:
            # Step 1: Check for abusive content using the AI service
            if self.ai_service.check_for_abuse(content):
                logger.warning("Email content flagged as abusive. Not queuing.")
                return False

            # Step 2: Create a domain model instance
            email = EmailMessage(
                recipient=recipient,
                subject=subject,
                content=content
            )

            # Step 3: Add the email to the repository
            self.email_repository.add_email(email)
            logger.info("Email successfully queued for sending.")
            return True

        except Exception as e:
            logger.error(f"An error occurred while queuing the email: {e}")
            return False
