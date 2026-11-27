from asyncio import timeout
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@asynccontextmanager
async def init_postgres(
    url: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine(
        url,
        pool_size=10,
        pool_recycle=1800,
        pool_pre_ping=True,
        hide_parameters=True,
    )
    try:
        async with timeout(10), engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        yield async_sessionmaker(bind=engine, expire_on_commit=False)
    finally:
        await engine.dispose()
