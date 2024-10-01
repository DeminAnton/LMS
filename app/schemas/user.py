from pydantic import BaseModel, EmailStr, constr

# Schema for creating a new user
class UserCreate(BaseModel):
    nickname: constr(min_length=3, max_length=50)
    email: EmailStr | None = None  # Optional email
    password: constr(min_length=8)  # Password should be at least 8 characters long

# Schema for updating user information
class UserUpdate(BaseModel):
    nickname: constr(min_length=3, max_length=50) | None = None  # Optional nickname
    email: EmailStr | None = None  # Optional email

# Schema for returning user information in responses
class UserOut(BaseModel):
    id: int
    nickname: str
    email: EmailStr | None = None
    role_id: int  # Assuming the role is returned as a string

    class Config:
        orm_mode = True  # Allows automatic conversion of SQLAlchemy objects to Pydantic models
