from datetime import datetime 

from pydantic import BaseModel, EmailStr 

from enum import Enum 

from typing import Optional 

 
class MessageStatus(str, Enum): 

    PENDING = "pending"    

    SENT = "sent"   

    FAILED = "failed"   



class EmailMessage(BaseModel): 

    id: str    

    recipient_email: EmailStr  

    subject: str   

    content: str     

    created_at: datetime   

    status: MessageStatus    

    access_code: str    

    encrypted_content: Optional[str] = None    

        

    class Config:    

        from_attributes = True        



class OneTimeCode(BaseModel): 

    code: str     

    created_at: datetime   

    used: bool = False   

    expires_at: datetime    

        

    class Config:     

        from_attributes = True      