from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.database import db_manager
from src.repositories.user_repo import UserRepo
from src.core.exceptions.auth import InvalidCredentialsException, InvalidExpireException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')
repo = UserRepo()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_manager.get_session),
):
    try:
        payload = jwt.decode(
            token, settings.app.secret_key, algorithms=[settings.app.algorithm]
        )
        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidCredentialsException()

        expire = payload.get('exp')
        if expire is None or datetime.utcnow() > datetime.fromtimestamp(expire):
            raise InvalidExpireException()

    except ExpiredSignatureError:
        raise InvalidExpireException()

    except JWTError as e:
        raise InvalidCredentialsException()

    user = await repo.get(session, int(user_id))
    if user is None:
        raise InvalidCredentialsException()
    return user
