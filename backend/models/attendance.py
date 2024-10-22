from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey,
    Text,
    Boolean
    )

from sqlalchemy.orm import relationship

class Attendance(Base):
    __tablename__ = 'attendences'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), primary_key=True)
    presence = Column(Boolean, nullable=False)
    comment = Column(Text)

    user = relationship("User", back_populates="attendances")
    lesson = relationship("Lesson", back_populates="attendances")