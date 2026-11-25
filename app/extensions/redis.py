from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from urllib.parse import parse_qs, unquote, urlsplit

from redis.asyncio import Redis


@asynccontextmanager
async def init_redis(url: str) -> AsyncIterator[Redis]:
    parsed = urlsplit(url)
    if not parsed.hostname:
        raise ValueError("REDIS_URL 必须指定主机地址")

    path_db = unquote(parsed.path.removeprefix("/"))
    query_db = parse_qs(parsed.query, keep_blank_values=True).get("db")
    if (query_db and not query_db[0]) or (not query_db and path_db and not path_db.isdecimal()):
        raise ValueError("REDIS_URL 的数据库编号必须为非负整数")

    async with Redis.from_url(
        url,
        decode_responses=True,
        max_connections=50,
        socket_timeout=5,
        socket_connect_timeout=5,
    ) as client:
        yield client
