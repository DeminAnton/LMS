from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey,
    Text,
    DateTime
    )

from sqlalchemy.orm import relationship


class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    start = Column(DateTime)
    comment = Column(Text)

    group = relationship("Group", back_populates="lessons")
    attendances = relationship("Attendance")