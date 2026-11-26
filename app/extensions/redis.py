from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis.asyncio import Redis


@asynccontextmanager
async def init_redis(url: str) -> AsyncGenerator[Redis, None]:
    async with Redis.from_url(
        url,
        decode_responses=True,
        max_connections=50,
        socket_timeout=5,
        socket_connect_timeout=5,
    ) as client:
        yield client
