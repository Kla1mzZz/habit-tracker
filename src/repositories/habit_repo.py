from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.habit import Habit
from src.models.user import User
from src.schemas.habit import HabitCreate


class HabitRepo:
    async def create(self, session: AsyncSession, habit: HabitCreate, user_id: int):
        user = await session.get(User, user_id)
        if not user:
            return None

        creating_habit = Habit(
            name=habit.name,
            description=habit.description,
            start_date=habit.start_date,
            status=habit.status,
            prediction_confidence=getattr(habit, '_prediction_confidence', 0.0),
            user_id=user.id,
        )

        session.add(creating_habit)

        await session.commit()
        await session.refresh(creating_habit)
        return creating_habit

    async def get(self, session: AsyncSession, habit_id: int):
        habit = await session.execute(
            select(Habit).filter(Habit.id == habit_id).options(selectinload(Habit.logs))
        )

        return habit.scalar_one_or_none()
