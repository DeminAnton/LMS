from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey,
    Text,
    )

from sqlalchemy.orm import relationship

class Topic(Base):
    __tablename__ = 'topics'

    topic_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.course_id'))
    title = Column(String(200))
    description = Column(Text)

    course = relationship("Course", back_populates="topics")
    blocks = relationship("Block", back_populates="topic")