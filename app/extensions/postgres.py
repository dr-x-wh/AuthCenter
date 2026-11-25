from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

NUMERIC_OPTIONS = {
    "timeout": float,
    "statement_cache_size": int,
    "max_cached_statement_lifetime": int,
    "max_cacheable_statement_size": int,
}


@asynccontextmanager
async def init_postgres(url: str) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database_url = make_url(url)
    query = dict(database_url.query)
    if not (database_url.host or query.get("host")):
        raise ValueError("DATABASE_URL must specify a host")
    if database_url.drivername in {"postgres", "postgresql"}:
        database_url = database_url.set(drivername="postgresql+asyncpg")
    if "sslmode" in query:
        query.setdefault("ssl", query.pop("sslmode"))
    connect_args = {
        name: convert(query.pop(name))
        for name, convert in NUMERIC_OPTIONS.items()
        if name in query
    }
    if "direct_tls" in query:
        direct_tls = query.pop("direct_tls")
        if direct_tls not in {"true", "false"}:
            raise ValueError("DATABASE_URL direct_tls must be true or false")
        connect_args["direct_tls"] = direct_tls == "true"

    engine = create_async_engine(
        database_url.set(query=query),
        connect_args=connect_args,
        pool_size=10,
        pool_recycle=1800,
        pool_pre_ping=True,
        hide_parameters=True,
    )
    try:
        yield async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    finally:
        await engine.dispose()
