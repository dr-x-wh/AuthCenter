from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

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
        yield async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    finally:
        await engine.dispose()
