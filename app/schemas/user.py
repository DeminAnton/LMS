from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List

class Role(BaseModel):
    role_id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True  # Enable ORM mode to work with SQLAlchemy objects


# Schema for creating a new user
class UserCreate(BaseModel):
    login: constr(min_length=3, max_length=50)
    email: EmailStr | None = None  # Optional email
    password: constr(min_length=8)  # Password should be at least 8 characters long
    first_name: constr(max_length=30)
    second_name: constr(max_length=30)
    role: str
    

# Schema for updating user information
class UserUpdate(BaseModel):
    login: constr(min_length=3, max_length=50) | None = None  # Optional nickname
    email: EmailStr | None = None  # Optional email

# Schema for returning user information in responses
class UserOut(BaseModel):
    user_id: int
    login: str
    email: EmailStr | None = None
    roles: List[Role]

    class Config:
        from_attributes = True  # Allows automatic conversion of SQLAlchemy objects to Pydantic models
