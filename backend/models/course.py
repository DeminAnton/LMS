from .base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .user import users_courses

class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)

    author = relationship("User", back_populates="courses")
    topics = relationship("Topic", back_populates="course")
    groups = relationship("Group", back_populates="course")
    students = relationship('User', secondary=users_courses, back_populates='courses')  # Many-to-many with users
