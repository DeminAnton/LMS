from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

class Enrollment(Base):
    user_id = Column(Integer, ForeignKey('user_table.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course_table.id'), primary_key=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow)