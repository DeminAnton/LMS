from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey,
    Text,
    UniqueConstraint,
    )

from sqlalchemy.orm import relationship

class Block(Base):
    __tablename__ = 'blocks'

    block_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    block_type_id = Column(Integer, ForeignKey('block_types.block_type_id'), nullable=False)
    title = Column(String(200), nullable=False)
    text = Column(Text)
    sequence = Column(Integer, nullable=False)

    topic = relationship("Topic", back_populates="blocks")
    block_type = relationship("BlockType", back_populates="blocks")
    attempts = relationship("Attempt", back_populates="block")

    __table_args__ = (
        UniqueConstraint('block_id', 'block_type_id', name='unique_block_type'),
        UniqueConstraint('topic_id', 'sequence', name='unique_topic_sequence')
    )