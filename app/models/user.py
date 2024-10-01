from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    nickname = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)  # Optional email
    password = Column(String(255), nullable=False)  # Hashed password
    role_id = Column(Integer, ForeignKey('role_table.id'), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    role_table = relationship("Role", back_populates="user_table")
    course_table = relationship("Course", secondary="enrollment_table", back_populates="user_table")

    # Hash the password before saving
    def hash_password(self, password: str):
        self.password = pwd_context.hash(password)

    # Verify password during login
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)