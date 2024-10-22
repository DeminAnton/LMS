from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text, Table, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

users_roles = Table(
    'users_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.role_id'), primary_key=True)
)

# Many-to-many relation between users and courses
users_courses = Table(
    'users_courses', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.course_id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False)
    second_name = Column(String(30), nullable=False)
    login = Column(String(20), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo = Column(String)
    about = Column(Text)
    
    # Relationships
    roles = relationship('Role', secondary=users_roles, back_populates='users')
    courses = relationship('Course', secondary=users_courses, back_populates='students')
    sessions = relationship('Session', back_populates='user')
    attempts = relationship('Attempt', back_populates='user')
    groups = relationship('Group', back_populates='supervisor')
    attendances = relationship('Attendance', back_populates='user')
    
    def __repr__(self):
        """String representation of the User model for debugging, including roles."""
        role_names = [role.name for role in self.roles]  # List comprehension to get all role names
        return (f"<User(user_id={self.user_id}, first_name={self.first_name}, "
                f"second_name={self.second_name}, login={self.login}, "
                f"email={self.email}, roles={role_names}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")