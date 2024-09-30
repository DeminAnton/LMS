from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Role(Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    
    # Relationship to users
    users = relationship("User", back_populates="role_table")