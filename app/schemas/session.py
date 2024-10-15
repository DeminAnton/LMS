from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    session_token: constr(min_length=254)
    created_at: datetime
    expires_at: datetime
    ip_address: constr(max_length=45)
    user_agent: constr(max_length=255)
    
