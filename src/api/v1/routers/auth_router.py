from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.database import db_manager
from src.repositories.user_repo import UserRepo
from src.core.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from src.schemas.auth import AuthResponse, AuthRegister
from src.core.config import settings
from src.core.exceptions.auth import (
    InvalidCredentialsException,
    AlreadyRegisteredException,
)

router = APIRouter(prefix='/auth', tags=['auth'])
repo = UserRepo()


@router.post('/register', response_model=AuthResponse)
async def register(
    user_data: AuthRegister, session: AsyncSession = Depends(db_manager.get_session)
):
    user_username = await repo.get_by_username(session, user_data.username)
    if user_username:
        raise AlreadyRegisteredException('Username')

    user_email = await repo.get_by_email(session, user_data.email)
    if user_email:
        raise AlreadyRegisteredException('Email')

    hashed_password = hash_password(user_data.password)

    creating_user = await repo.create(session, user_data, hashed_password)

    access_token_expires = timedelta(minutes=settings.app.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(creating_user.id)}, expires_delta=access_token_expires
    )

    return AuthResponse(access_token=access_token, token_type='bearer')


@router.post('/login', response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_manager.get_session),
):
    user = await repo.get_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=settings.app.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(user.id)}, expires_delta=access_token_expires
    )

    return AuthResponse(access_token=access_token, token_type='bearer')
