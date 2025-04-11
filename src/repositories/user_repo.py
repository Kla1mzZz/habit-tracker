from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.user import UserRegister
from src.models.user import User


class UserRepo:
    async def create(
        self, session: AsyncSession, user_data: UserRegister, hashed_password: str
    ):
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def get(self, session: AsyncSession, user_id: int):
        user = await session.execute(
            select(User).filter(User.id == user_id).options(selectinload(User.habits))
        )

        return user.scalar_one_or_none()

    async def get_by_username(self, session: AsyncSession, username: str):
        query = await session.execute(select(User).filter(User.username == username))

        user = query.scalar_one_or_none()

        return user

    async def get_by_email(self, session: AsyncSession, email: str):
        query = await session.execute(select(User).filter(User.email == email))

        user = query.scalar_one_or_none()

        return user
