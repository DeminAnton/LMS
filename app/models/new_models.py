from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table: users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    second_name = Column(String(30))
    login = Column(String(20), unique=True, nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    photo = Column(String)
    about = Column(Text)

    roles = relationship("UserRole", back_populates="user")
    students = relationship("Student", back_populates="user")
    teachers = relationship("Teacher", back_populates="user")
    attempts = relationship("Attempt", back_populates="user")

# Table: roles
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)
    description = Column(String(200))

    users = relationship("UserRole", back_populates="role")

# Junction Table: UserRole (Many-to-Many between Users and Roles)
class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

# Table: students
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="students")
    courses = relationship("StudentCourse", back_populates="student")

# Table: teachers
class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="teachers")
    courses = relationship("Course", back_populates="author")
    groups = relationship("Group", back_populates="supervisor")

# Table: course
class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    authors_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)

    author = relationship("Teacher", back_populates="courses")
    students = relationship("StudentCourse", back_populates="course")
    topics = relationship("Topic", back_populates="course")

# Junction Table: StudentCourse (Many-to-Many between Students and Courses)
class StudentCourse(Base):
    __tablename__ = 'student_courses'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")

# Table: topic
class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    title = Column(String(200))
    description = Column(Text)

    course = relationship("Course", back_populates="topics")
    blocks = relationship("Block", back_populates="topic")

# Table: block
class Block(Base):
    __tablename__ = 'block'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)
    title = Column(String(200), nullable=False)
    text = Column(Text)
    sequence = Column(Integer, nullable=False)

    topic = relationship("Topic", back_populates="blocks")
    type = relationship("Type", back_populates="blocks")
    attempts = relationship("Attempt", back_populates="block")

    __table_args__ = (
        UniqueConstraint('id', 'type_id', name='unique_block_type'),
        UniqueConstraint('topic_id', 'sequence', name='unique_topic_sequence')
    )

# Table: types
class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), unique=True, nullable=False)

    blocks = relationship("Block", back_populates="type")

# Table: attempt
class Attempt(Base):
    __tablename__ = 'attempt'

    id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey('block.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    attempted_at = Column(DateTime, nullable=False)
    input = Column(Text)
    output = Column(Text)
    success = Column(Boolean)
    comment = Column(String)

    block = relationship("Block", back_populates="attempts")
    user = relationship("User", back_populates="attempts")

# Table: group
class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    supervisor = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))

    lessons = relationship("Lesson", back_populates="group")
    teacher = relationship("Teacher", back_populates="groups")

# Table: lesson
class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    start = Column(DateTime)
    comment = Column(Text)

    group = relationship("Group", back_populates="lessons")
