from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error: str,
        details: str | None = None,
        code: str | None = None,
        headers: Dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={'error': error, 'details': details, 'code': code},
            headers=headers,
        )


class NotFoundException(CustomHTTPException):
    def __init__(self, entity: str = 'Entity'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error=f'{entity} not found',
            code='not_found',
        )
