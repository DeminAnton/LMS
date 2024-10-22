from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .user import users_roles

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)
    description = Column(String(200))

    users = relationship('User', secondary=users_roles, back_populates='roles')