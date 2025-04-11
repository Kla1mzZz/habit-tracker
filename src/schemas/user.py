from typing import List
from pydantic import BaseModel, Field, EmailStr

from src.schemas.habit import HabitResponse


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserRegister(UserBase):
    password: str


class UserLogin(UserBase):
    username: str
    password: str


class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str
