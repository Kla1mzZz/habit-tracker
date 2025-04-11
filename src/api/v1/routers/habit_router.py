import logging

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.exceptions.http import NotFoundException
from src.schemas.habit import (
    HabitBase,
    HabitCreate,
    HabitResponse,
    HabitRequest,
    HabitsListResponse,
)
from src.schemas.user import UserResponse
from src.models.user import User
from src.repositories.habit_repo import HabitRepo
from src.repositories.user_repo import UserRepo
from src.database import db_manager


logger = logging.getLogger('api.v1.habits')

router = APIRouter(prefix='/habits', tags=['habit'])
repo = HabitRepo()


@router.get('/', response_model=HabitsListResponse)
async def get_habits(user: User = Depends(get_current_user)):
    habits = user.habits

    return {'data': habits}


@router.get('/{id}', response_model=HabitResponse)
async def get_habit(
    id: int,
    session: AsyncSession = Depends(db_manager.get_session),
    user: User = Depends(get_current_user),
):
    habit = await repo.get(session, id)

    if habit:
        return habit

    raise NotFoundException('Habit')


@router.post('/', response_model=HabitResponse)
async def create_habit(
    habit: HabitCreate,
    session: AsyncSession = Depends(db_manager.get_session),
    user: User = Depends(get_current_user),
):
    created_habit = await repo.create(session, habit, user.id)

    if created_habit:
        return HabitResponse(
            name=created_habit.name,
            description=created_habit.description,
            start_date=created_habit.start_date,
            status=created_habit.status,
            id=created_habit.id,
            prediction_confidence=created_habit.prediction_confidence,
        )

    raise NotFoundException('User')
