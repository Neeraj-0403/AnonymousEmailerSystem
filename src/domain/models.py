# domain/models.py

from dataclasses import dataclass
from datetime import datetime

# Represents the core entity for an email message in the system.
@dataclass
class EmailMessage:
    recipient: str
    subject: str
    content: str
    id: int = 0
    is_sent: bool = False
    sent_timestamp: datetime = None

# Represents a one-time access code.
@dataclass
class AuthCode:
    code: str
    is_used: bool = False
