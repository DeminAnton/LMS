from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    )

from sqlalchemy.orm import relationship


class BlockType(Base):
    __tablename__ = 'block_types'

    block_type_id = Column(Integer, primary_key=True)
    block_type = Column(String(10), unique=True, nullable=False)

    blocks = relationship("Block", back_populates="block_type")
