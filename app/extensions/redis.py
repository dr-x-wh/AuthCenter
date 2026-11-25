from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from urllib.parse import parse_qs, unquote, urlsplit

from redis.asyncio import Redis


@asynccontextmanager
async def init_redis(url: str) -> AsyncIterator[Redis]:
    parsed = urlsplit(url)
    path_db = unquote(parsed.path.removeprefix("/"))
    query_db = parse_qs(parsed.query, keep_blank_values=True).get("db", [])
    for database in (path_db or "0", *query_db):
        if not database.isascii() or not database.isdecimal():
            raise ValueError("REDIS_URL database index must be a non-negative integer")

    async with AsyncExitStack() as stack:
        try:
            client = Redis.from_url(
                url,
                decode_responses=True,
                max_connections=50,
                socket_timeout=5,
                socket_connect_timeout=5,
            )
            stack.push_async_callback(client.aclose)
            client.connection_pool.make_connection()  # Check options without opening a socket.
        except (TypeError, ValueError):
            raise ValueError("REDIS_URL contains invalid Redis connection options") from None
        yield client
