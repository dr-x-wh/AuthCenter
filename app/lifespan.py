from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings
from app.extensions import init_postgres, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings: Settings = app.state.settings

    async with (
        init_postgres(settings.database_url) as session_factory,
        init_redis(settings.redis_url) as redis,
    ):
        app.state.session_factory = session_factory
        app.state.redis = redis
        try:
            yield
        finally:
            del app.state.session_factory
            del app.state.redis
