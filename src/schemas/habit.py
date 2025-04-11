from typing import List
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, PrivateAttr

from src.enums import HabitStatus


class HabitBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(None, max_length=100)
    start_date: datetime
    status: HabitStatus


class HabitCreate(HabitBase):
    status: HabitStatus = HabitStatus.pending

    _prediction_confidence: float = PrivateAttr(0.0)

    start_date: datetime = datetime.now()


class HabitLogResponse(BaseModel):
    habit_id: int
    date: datetime
    status: HabitStatus
    notes: str | None = None
    user_id: int

    class Config:
        from_attributes = True


class HabitResponse(HabitBase):
    id: int
    prediction_confidence: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description='Вероятность выполнения привычки, рассчитанная нейросетью',
    )

    logs: List[HabitLogResponse] | None = None

    class Config:
        from_attributes = True


class HabitsListResponse(BaseModel):
    data: List[HabitResponse]


class HabitRequest(HabitBase):
    id: int
