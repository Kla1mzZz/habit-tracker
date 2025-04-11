from typing import List
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.enums import HabitStatus


class Habit(Base):
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[HabitStatus] = mapped_column(
        String, default=HabitStatus.pending, nullable=False
    )
    prediction_confidence: Mapped[float] = mapped_column(Float, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='habits')

    logs: Mapped[List['HabitLog']] = relationship('HabitLog', back_populates='habit')


class HabitLog(Base):
    habit_id: Mapped[int] = mapped_column(Integer, ForeignKey('habits.id'))
    date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    status: Mapped[HabitStatus] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
    )

    habit: Mapped[Habit] = relationship('Habit', back_populates='logs')
