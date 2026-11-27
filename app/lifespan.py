from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from app.extensions import init_postgres, init_redis

if TYPE_CHECKING:
    from app.core.config import Settings


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
