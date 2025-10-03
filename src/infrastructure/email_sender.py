# infrastructure/email_sender.py

import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from infrastructure.logger import logger

class EmailSender:
    """
    A service to handle the actual sending of emails.
    This is a mock implementation for demonstration.
    """
    def __init__(self):
        # SMTP configuration - use environment variables for security
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
        logger.info("Email sender service initialized.")

    def send_email(self, recipient: str, subject: str, content: str) -> bool:
        """
        Sends an actual email using SMTP.
        
        Args:
            recipient (str): The recipient's email address.
            subject (str): The email subject.
            content (str): The email body.
            
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
            logger.info(f"Attempting to send email to {recipient}...")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(content, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient}.")
            logger.debug(f"Subject: {subject}")
            logger.debug(f"Content: {content[:50]}...") # Show a snippet of content
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            return False
