from datetime import datetime
from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    DateTime, 
    Boolean, 
    Index, 
    UniqueConstraint
    )

from sqlalchemy.orm import relationship

class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    session_key = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_active_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45))  # Can handle IPv4 and IPv6
    user_agent = Column(String(255))
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index('ix_user_id', 'user_id'),
        UniqueConstraint('session_token', name='unique_session_token'),
    )
