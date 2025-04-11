import logging
from typing import Dict, Any

from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse

from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    OperationalError,
)


logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request, exc: IntegrityError) -> ORJSONResponse:
        logger.error('Database integrity error', exc_info=exc)
        return _build_error_response(
            message='Data integrity violation',
            details=str(exc.orig),
            status_code=status.HTTP_409_CONFLICT,
            error_type='integrity_error',
        )

    @app.exception_handler(OperationalError)
    async def handle_operational_error(
        request, exc: OperationalError
    ) -> ORJSONResponse:
        logger.critical('Database operational error', exc_info=exc)
        return _build_error_response(
            message='Database connection error',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_type='database_unavailable',
        )

    @app.exception_handler(DatabaseError)
    async def handle_database_error(request, exc: DatabaseError) -> ORJSONResponse:
        logger.error('Unhandled database error', exc_info=exc)
        return _build_error_response(
            message='Database operation failed',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type='database_error',
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception) -> ORJSONResponse:
        logger.critical('Unhandled exception', exc_info=exc)
        return _build_error_response(
            message='Internal server error',
            details=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type='internal_error',
        )


def _build_error_response(
    message: str,
    status_code: int,
    error_type: str,
    details: str | None = None,
    **extra: Dict[str, Any],
) -> ORJSONResponse:
    content = {'error': {'type': error_type, 'message': message, 'code': status_code}}
    if details:
        content['error']['details'] = details
    if extra:
        content['error']['extra'] = extra

    return ORJSONResponse(
        content=content,
        status_code=status_code,
        headers={'Cache-Control': 'no-store', 'X-Error-Type': error_type},
    )
