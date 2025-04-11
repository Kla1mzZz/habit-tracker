from typing import List

from sqlalchemy import Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.habit import Habit


class User(Base):
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    habits: Mapped[List['Habit']] = relationship('Habit', back_populates='user')
