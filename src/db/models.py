from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass
