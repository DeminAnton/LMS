from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Course(Base):
    title = Column(String(100), nullable=False)
    description = Column(String)

    # Relationship to users (students)
    user_table = relationship("User", secondary="enrollment_table", back_populates="course_table")
