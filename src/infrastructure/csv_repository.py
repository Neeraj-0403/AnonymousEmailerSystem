# infrastructure/csv_repository.py

import os
import pandas as pd
from typing import List, Optional
from domain.auth_repository import AuthRepository
from domain.email_repository import EmailRepository
from domain.models import AuthCode, EmailMessage
from infrastructure.logger import logger
from infrastructure.encryption_service import EncryptionService

class CSVRepository(AuthRepository, EmailRepository):
    """
    Concrete repository implementation using CSV files.
    It handles both authentication codes and email message storage.
    """
    def __init__(self, auth_file: str, email_file: str, encryption_service: EncryptionService):
        self.auth_file = auth_file
        self.email_file = email_file
        self.encryption_service = encryption_service

        # Ensure CSV files exist with correct headers
        self._check_and_create_files()
        logger.info("CSV repository initialized.")

    def _check_and_create_files(self):
        """Creates CSV files with headers if they don't exist."""
        try:
            if not os.path.exists(self.auth_file):
                df = pd.DataFrame(columns=['code', 'is_used'])
                df.to_csv(self.auth_file, index=False)
                logger.info(f"Created new CSV file: {self.auth_file}")

            if not os.path.exists(self.email_file):
                df = pd.DataFrame(columns=['id', 'recipient', 'subject', 'encrypted_content', 'is_sent', 'sent_timestamp'])
                df.to_csv(self.email_file, index=False)
                logger.info(f"Created new CSV file: {self.email_file}")
        except Exception as e:
            logger.error(f"Error creating CSV files: {e}")
            raise

    # --- AuthRepository Implementation ---
    def get_auth_code(self, code: str) -> Optional[AuthCode]:
        """Reads auth codes from CSV and finds a matching unused code."""
        try:
            df = pd.read_csv(self.auth_file)
            code_row = df[(df['code'] == code) & (df['is_used'] == False)]
            if not code_row.empty:
                logger.info(f"Auth code '{code}' found and is unused.")
                return AuthCode(code=code_row.iloc[0]['code'], is_used=code_row.iloc[0]['is_used'])
            else:
                logger.warning(f"Auth code '{code}' not found or already used.")
                return None
        except Exception as e:
            logger.error(f"Error getting auth code from CSV: {e}")
            return None

    def update_auth_code_status(self, code: str, is_used: bool) -> None:
        """Updates the status of an auth code in the CSV file."""
        try:
            df = pd.read_csv(self.auth_file)
            df.loc[df['code'] == code, 'is_used'] = is_used
            df.to_csv(self.auth_file, index=False)
            logger.info(f"Auth code '{code}' status updated to 'is_used': {is_used}.")
        except Exception as e:
            logger.error(f"Error updating auth code status: {e}")
            raise

    # --- EmailRepository Implementation ---
    def add_email(self, email: EmailMessage) -> None:
        """Appends a new email record to the emails CSV file."""
        try:
            df_emails = pd.read_csv(self.email_file)
            # Find the next available ID
            email.id = df_emails['id'].max() + 1 if not df_emails.empty else 1
            
            # Encrypt the content before saving
            encrypted_content = self.encryption_service.encrypt(email.content)

            new_row = {
                'id': email.id,
                'recipient': email.recipient,
                'subject': email.subject,
                'encrypted_content': encrypted_content,
                'is_sent': False,
                'sent_timestamp': None
            }
            
            # Using concat to add a new row to the DataFrame
            new_df = pd.DataFrame([new_row])
            df_emails = pd.concat([df_emails, new_df], ignore_index=True)
            
            df_emails.to_csv(self.email_file, index=False)
            logger.info(f"Email with ID {email.id} queued for sending.")
        except Exception as e:
            logger.error(f"Error adding email to CSV: {e}")
            raise

    def get_emails_to_send(self, limit: int) -> List[EmailMessage]:
        """Retrieves unsent emails from the CSV file."""
        emails = []
        try:
            df = pd.read_csv(self.email_file)
            df_to_send = df[(df['is_sent'] == False)].head(limit)
            
            if df_to_send.empty:
                logger.info("No new emails to send found.")
                return emails
            
            for _, row in df_to_send.iterrows():
                email_id = int(row['id'])
                encrypted_content = row['encrypted_content']
                
                # Decrypt the content for use in the job
                decrypted_content = self.encryption_service.decrypt(encrypted_content)
                
                email = EmailMessage(
                    id=email_id,
                    recipient=row['recipient'],
                    subject=row['subject'],
                    content=decrypted_content,
                    is_sent=row['is_sent']
                )
                emails.append(email)
            
            logger.info(f"Retrieved {len(emails)} emails to send.")
            return emails
        except Exception as e:
            logger.error(f"Error getting emails from CSV: {e}")
            return []

    def update_email_status(self, email_id: int, is_sent: bool) -> None:
        """Updates the sent status of an email record in the CSV file."""
        try:
            df = pd.read_csv(self.email_file)
            df.loc[df['id'] == email_id, 'is_sent'] = is_sent
            df.loc[df['id'] == email_id, 'sent_timestamp'] = pd.Timestamp.now()
            df.to_csv(self.email_file, index=False)
            logger.info(f"Email with ID {email_id} status updated to 'is_sent': {is_sent}.")
        except Exception as e:
            logger.error(f"Error updating email status: {e}")
            raise

def recreate_auth_file(auth_file):
    """Recreates the auth_codes.csv file with valid CSV format."""
    data = {
        'code': ['ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345', 'PQR678', 'STU901', 'VWX234', 'YZA567', 'BCD890'],
        'is_used': [False] * 10
    }
    df = pd.DataFrame(data)
    df.to_csv(auth_file, index=False)

# Call this function to recreate the file
recreate_auth_file('auth_codes.csv')