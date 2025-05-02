from loguru import logger
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.routers.habit_router import router as habit_router
from src.api.v1.routers.auth_router import router as auth_router

from src.core.config import settings
from src.database import db_manager
from src.core.exceptions.handler import setup_exception_handlers
from src.ml.model_service import model_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        logger.info('Initializing ML model')
        model_service.load_model()
        app.state.model_service = model_service
        logger.info('Model loaded successfully')
    except Exception as e:
        logger.critical(f'Failed to load model: {str(e)}')
        raise
    
    yield

    logger.info('Shutting down the application...')
    logger.info('Dispose engine')
    await db_manager.dispose()


def get_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan, **settings.app.model_dump())

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(habit_router, prefix=settings.app.prefix.v1)
    app.include_router(auth_router, prefix=settings.app.prefix.v1)

    setup_exception_handlers(app)

    return app


app = get_application()
