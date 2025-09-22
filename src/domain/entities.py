from datetime import datetimefrom datetime import datetime

from pydantic import BaseModel, EmailStrfrom pydantic import BaseModel, EmailStr

from enum import Enumfrom enum import Enum

from typing import Optionalfrom typing import Optional



class MessageStatus(str, Enum):class MessageStatus(str, Enum):

    PENDING = "pending"    PENDING = "pending"

    SENT = "sent"    SENT = "sent"

    FAILED = "failed"    FAILED = "failed"



class EmailMessage(BaseModel):class EmailMessage(BaseModel):

    id: str    id: str

    recipient_email: EmailStr    recipient_email: EmailStr

    subject: str    subject: str

    content: str    content: str

    created_at: datetime    created_at: datetime

    status: MessageStatus    status: MessageStatus

    access_code: str    access_code: str

    encrypted_content: Optional[str] = None    encrypted_content: Optional[str] = None

        

    class Config:    class Config:

        from_attributes = True        from_attributes = True



class OneTimeCode(BaseModel):class OneTimeCode(BaseModel):

    code: str    code: str

    created_at: datetime    created_at: datetime

    used: bool = False    used: bool = False

    expires_at: datetime    expires_at: datetime

        

    class Config:    class Config:

        from_attributes = True        from_attributes = True