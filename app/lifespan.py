from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from app.core import get_settings
from app.extensions import init_postgres, init_redis
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    async with AsyncExitStack() as stack:
        # PostgreSQL
        app.state.session_factory = (await stack.enter_async_context(init_postgres(settings.postgres_url)))
        # Redis
        app.state.redis = (await stack.enter_async_context(init_redis(settings.redis_url)))
        logger.info("Application startup completed")
        try:
            yield
        finally:
            del app.state.session_factory
            del app.state.redis
    logger.info("Application shutdown completed")
