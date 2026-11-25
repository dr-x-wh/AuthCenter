from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from inspect import signature

from asyncpg import connect
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

CONNECT_OPTIONS = (
    signature(connect).parameters.keys()
    - {"connection_class", "dsn", "loop", "record_class", "server_settings"}
    | {"prepared_statement_cache_size"}
)
NUMERIC_OPTIONS = {
    "timeout": float,
    "statement_cache_size": int,
    "max_cached_statement_lifetime": int,
    "max_cacheable_statement_size": int,
}


@asynccontextmanager
async def init_postgres(url: str) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    try:
        database_url = make_url(url).set(drivername="postgresql+asyncpg")
        if "sslmode" in database_url.query and "ssl" not in database_url.query:
            sslmode = database_url.query["sslmode"]
            database_url = database_url.difference_update_query(["sslmode"]).update_query_dict(
                {"ssl": sslmode},
            )
        if database_url.query.keys() - CONNECT_OPTIONS:
            raise ValueError("Unsupported asyncpg connection option")
        connect_args = {
            name: convert(database_url.query[name])
            for name, convert in NUMERIC_OPTIONS.items()
            if name in database_url.query
        }
        if "direct_tls" in database_url.query:
            direct_tls = database_url.query["direct_tls"]
            if direct_tls not in {"true", "false"}:
                raise ValueError("Invalid direct_tls value")
            connect_args["direct_tls"] = direct_tls == "true"
        engine = create_async_engine(
            database_url,
            connect_args=connect_args,
            pool_size=10,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            hide_parameters=True,
        )
    except (ArgumentError, TypeError, ValueError):
        raise ValueError("DATABASE_URL contains invalid PostgreSQL connection options") from None

    try:
        yield async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    finally:
        await engine.dispose()
