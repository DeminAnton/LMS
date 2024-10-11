from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Table: users
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)  # Renamed 'id' to 'user_id'
    first_name = Column(String(30), nullable=False)
    second_name = Column(String(30), nullable=False)
    login = Column(String(20), unique=True, nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo = Column(String)
    about = Column(Text)

    roles = relationship("Role", back_populates="users")
    sessions = relationship("Session", back_populates="user")
    attempts = relationship("Attempt", back_populates="user")
    groups = relationship("Group", back_populates="supervisor")

# Table: roles
class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'role_id'
    name = Column(String(10), unique=True, nullable=False)
    description = Column(String(200))

    users = relationship("User", back_populates="roles")


# Table: course
class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'course_id'
    title = Column(String(200), nullable=False)
    description = Column(Text)

    users = relationship("User", back_populates="courses")
    topics = relationship("Topic", back_populates="course")
    groups = relationship("Group", back_populates="course")


# Table: topics
class Topic(Base):
    __tablename__ = 'topics'

    topic_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'topic_id'
    title = Column(String(200))
    description = Column(Text)

    blocks = relationship("Block", back_populates="topic")


# Table: blocks
class Block(Base):
    __tablename__ = 'blocks'

    block_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'block_id'
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


# Table: block_types
class BlockType(Base):
    __tablename__ = 'block_types'

    block_type_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'block_type_id'
    block_type = Column(String(10), unique=True, nullable=False)

    blocks = relationship("Block", back_populates="block_type")


# Table: attempts
class Attempt(Base):
    __tablename__ = 'attempts'

    attempt_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'attempt_id'
    block_id = Column(Integer, ForeignKey('blocks.block_id'))  # Renamed from 'id' to 'block_id'
    user_id = Column(Integer, ForeignKey('users.user_id'))
    attempted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    input = Column(Text)
    output = Column(Text)
    success = Column(Boolean)
    comment = Column(String)

    block = relationship("Block", back_populates="attempts")
    user = relationship("User", back_populates="attempts")


# Table: groups
class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'group_id'
    name = Column(String(50), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.course_id'))

    supervisor = relationship("User", back_populates="groups")
    lessons = relationship("Lesson", back_populates="group")


# Table: lessons
class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True)  # Renamed 'id' to 'lesson_id'
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)  # Renamed 'id' to 'group_id'
    start = Column(DateTime)
    comment = Column(Text)

    group = relationship("Group", back_populates="lessons")


# Table: attendences
class Attendance(Base):
    __tablename__ = 'attendences'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), primary_key=True)  # Renamed 'id' to 'lesson_id'
    presence = Column(Boolean, nullable=False)
    comment = Column(Text)

    user = relationship("User", back_populates="attendances")
    lesson = relationship("Lesson", back_populates="attendances")


# Table: sessions
class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)  # Renamed from 'id' to 'session_id'
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_active_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45))  # Can handle IPv4 and IPv6
    user_agent = Column(String(255))
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index('ix_user_id', 'user_id'),
        UniqueConstraint('session_token', name='unique_session_token'),
    )
