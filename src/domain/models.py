# domain/models.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmailMessage:
    recipient: str
    subject: str
    content: str
    id: int = 0
    is_sent: bool = False
    sent_timestamp: datetime = None
