# jobs/sender_job.py

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.csv_repository import CSVRepository
from infrastructure.email_sender import EmailSender
from infrastructure.encryption_service import EncryptionService
from infrastructure.logger import setup_logger, logger

def run_email_job():
    """
    The main function for the email sender job.
    It retrieves and sends a batch of queued emails.
    """
    try:
        if logger is None:
            print("Logger setup failed. Exiting.")
            return

        logger.info("Starting the email sender job...")

        # Initialize infrastructure components
        encryption_service = EncryptionService()
        email_repository = CSVRepository(email_file='data/emails_to_send.csv', encryption_service=encryption_service)
        email_sender = EmailSender()

        # Get the next batch of emails to send (e.g., up to 10 records)
        emails_to_send = email_repository.get_emails_to_send(limit=10)

        if not emails_to_send:
            logger.info("No emails to send. Job finished.")
            return

        # Process each email in the batch
        for email in emails_to_send:
            try:
                # Send the email
                is_sent = email_sender.send_email(
                    recipient=email.recipient,
                    subject=email.subject,
                    content=email.content
                )

                if is_sent:
                    # Update the status in the repository
                    email_repository.update_email_status(email_id=email.id, is_sent=True)
                else:
                    logger.error(f"Failed to send email with ID {email.id}. It will remain in the queue.")

            except Exception as e:
                logger.error(f"An unexpected error occurred while processing email with ID {email.id}: {e}")

        logger.info("Email sender job completed.")

    except Exception as e:
        logger.critical(f"A critical error occurred in the email sender job: {e}")

if __name__ == "__main__":
    run_email_job()
