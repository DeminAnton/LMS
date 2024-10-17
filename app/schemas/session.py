from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    session_token: str
    ip_address: constr(max_length=45)
    user_agent: constr(max_length=255)
    
