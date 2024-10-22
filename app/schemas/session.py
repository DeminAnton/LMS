from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    session_key: str
    ip_address: constr(max_length=45)
    user_agent: constr(max_length=255)
    
class SessionGet(BaseModel):
    session_id: int
    user_id: int
    session_key: constr(min_length=25)
    created_at: datetime
    expires_at: datetime
    last_active_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool
    
    class Config:
        from_attributes = True  # Enable ORM mode to work with SQLAlchemy objects
