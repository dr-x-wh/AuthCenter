from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from redis.asyncio import Redis


@asynccontextmanager
async def init_redis(url: str) -> AsyncIterator[Redis]:
    client = Redis.from_url(
        url,
        decode_responses=True,
        max_connections=50,
        socket_timeout=5,
        socket_connect_timeout=5,
    )
    try:
        yield client
    finally:
        await client.aclose()
