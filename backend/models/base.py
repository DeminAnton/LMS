from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
