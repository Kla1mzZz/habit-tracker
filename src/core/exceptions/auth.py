from fastapi import status

from src.core.exceptions.http import CustomHTTPException


class InvalidCredentialsException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error='Invalid credentials',
            code='invalid_credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class AlreadyRegisteredException(CustomHTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=f'{field} already registered',
            details=f'{field} you provided is already in use',
            code='already_registered',
        )


class InvalidExpireException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error='The authentication token has expired',
            code='invalid_expire',
            headers={'WWW-Authenticate': 'Bearer'},
        )
