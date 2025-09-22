# infrastructure/email_sender.py

import time
from infrastructure.logger import logger

class EmailSender:
    """
    A service to handle the actual sending of emails.
    This is a mock implementation for demonstration.
    """
    def __init__(self):
        # In a real application, this would be initialized with SMTP credentials.
        logger.info("Email sender service initialized.")

    def send_email(self, recipient: str, subject: str, content: str) -> bool:
        """
        Simulates sending an email to a recipient.
        In a real application, this would use a library like smtplib.
        
        Args:
            recipient (str): The recipient's email address.
            subject (str): The email subject.
            content (str): The email body.
            
        Returns:
            bool: True if the email was "sent" successfully, False otherwise.
        """
        try:
            logger.info(f"Attempting to send email to {recipient}...")
            # Simulate network delay for sending the email
            time.sleep(1)
            
            # For demonstration, we'll assume it's always successful.
            logger.info(f"Email sent successfully to {recipient}.")
            logger.debug(f"Subject: {subject}")
            logger.debug(f"Content: {content[:50]}...") # Show a snippet of content
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            return False
