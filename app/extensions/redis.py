from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis.asyncio import Redis
from redis.maint_notifications import MaintNotificationsConfig


@asynccontextmanager
async def init_redis(url: str) -> AsyncGenerator[Redis, None]:
    async with Redis.from_url(
        url,
        decode_responses=True,
        max_connections=50,
        socket_timeout=5,
        socket_connect_timeout=5,
        maint_notifications_config=MaintNotificationsConfig(enabled=False),
    ) as client:
        yield client
