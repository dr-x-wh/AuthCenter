from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
    factory = cast(async_sessionmaker[AsyncSession], request.app.state.session_factory, )

    async with factory() as session:
        yield session


def get_redis(request: Request) -> Redis:
    return cast(Redis, request.app.state.redis)


DBSession = Annotated[AsyncSession, Depends(get_db),]

RedisClient = Annotated[Redis, Depends(get_redis),]
