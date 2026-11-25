from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import Settings
from app.core.logging import configure_logging, logger
from app.extensions import init_postgres, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    configure_logging(settings.log_level.upper())

    async with (
        init_postgres(settings.database_url) as session_factory,
        init_redis(settings.redis_url) as redis,
    ):
        app.state.session_factory = session_factory
        app.state.redis = redis

        logger.info("Application startup completed, environment=%s", settings.environment)
        try:
            yield
        finally:
            del app.state.session_factory
            del app.state.redis
    logger.info("Application shutdown completed")
