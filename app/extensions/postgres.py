from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@asynccontextmanager
async def init_postgres(url: str) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database_url = make_url(url)
    if database_url.drivername in {"postgres", "postgresql"}:
        database_url = database_url.set(drivername="postgresql+asyncpg")

    engine = create_async_engine(
        database_url,
        pool_size=10,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        hide_parameters=True,
    )
    try:
        yield async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    finally:
        await engine.dispose()
