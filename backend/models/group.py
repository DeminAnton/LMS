from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey,
    )

from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.course_id'))

    supervisor = relationship("User", back_populates="groups")
    lessons = relationship("Lesson", back_populates="group")
    course = relationship("Course", back_populates="groups")
