from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from app.core.logging import configure_logging, logger
from app.extensions import init_postgres, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = app.state.settings
    configure_logging(settings.log_level.upper())

    async with AsyncExitStack() as stack:
        session_factory = await stack.enter_async_context(init_postgres(str(settings.database_url)))
        redis = await stack.enter_async_context(init_redis(str(settings.redis_url)))
        app.state.session_factory = session_factory
        app.state.redis = redis

        logger.info("Application startup completed, environment=%s", settings.environment)
        try:
            yield
        finally:
            del app.state.session_factory
            del app.state.redis
    logger.info("Application shutdown completed")
