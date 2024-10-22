from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Text, 
    Boolean, 
    ForeignKey,
    DateTime, 
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base



class Attempt(Base):
    __tablename__ = 'attempts'

    attempt_id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey('blocks.block_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    attempted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    input = Column(Text)
    output = Column(Text)
    success = Column(Boolean)
    comment = Column(String)

    block = relationship("Block", back_populates="attempts")
    user = relationship("User", back_populates="attempts")