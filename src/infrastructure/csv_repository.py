# infrastructure/csv_repository.py

import os
import pandas as pd
from typing import List
from domain.email_repository import EmailRepository
from domain.models import EmailMessage
from infrastructure.logger import logger
from infrastructure.encryption_service import EncryptionService
from datetime import datetime

class CSVRepository(EmailRepository):
    def __init__(self, email_file: str, encryption_service: EncryptionService):
        self.email_file = email_file
        self.encryption_service = encryption_service
        self._check_and_create_files()

    def _check_and_create_files(self):
        if not os.path.exists(self.email_file):
            df = pd.DataFrame(columns=['id', 'recipient', 'subject', 'encrypted_content', 'is_sent', 'sent_timestamp'])
            df.to_csv(self.email_file, index=False)

    def add_email(self, email: EmailMessage) -> None:
        df_emails = pd.read_csv(self.email_file)
        email.id = df_emails['id'].max() + 1 if not df_emails.empty else 1
        encrypted_content = self.encryption_service.encrypt(email.content)
        new_row = {
            'id': email.id,
            'recipient': email.recipient,
            'subject': email.subject,
            'encrypted_content': encrypted_content,
            'is_sent': False,
            'sent_timestamp': datetime.now().isoformat()
        }
        new_df = pd.DataFrame([new_row])
        df_emails = pd.concat([df_emails, new_df], ignore_index=True)
        df_emails.to_csv(self.email_file, index=False)

    def get_emails_to_send(self, limit: int) -> List[EmailMessage]:
        emails = []
        df = pd.read_csv(self.email_file)
        df_to_send = df[(df['is_sent'] == False)].head(limit)
        for _, row in df_to_send.iterrows():
            email_id = int(row['id'])
            encrypted_content = row['encrypted_content']
            decrypted_content = self.encryption_service.decrypt(encrypted_content)
            email = EmailMessage(
                id=email_id,
                recipient=row['recipient'],
                subject=row['subject'],
                content=decrypted_content,
                is_sent=row['is_sent']
            )
            emails.append(email)
        return emails

    def update_email_status(self, email_id: int, is_sent: bool) -> None:
        df = pd.read_csv(self.email_file)
        df.loc[df['id'] == email_id, 'is_sent'] = is_sent
        df.loc[df['id'] == email_id, 'sent_timestamp'] = pd.Timestamp.now()
        df.to_csv(self.email_file, index=False)