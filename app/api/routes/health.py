from asyncio import timeout

from asyncpg import InterfaceError, PostgresError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..deps import DBSession, RedisClient

router = APIRouter(prefix="/health", tags=["健康检查"])
READINESS_TIMEOUT = 3

health_up = {"status": "UP"}
health_down = {"status": "DOWN"}


@router.get("")
@router.get("/live")
@router.get("/startup")
async def live() -> dict:
    return health_up


@router.get("/ready")
async def ready(db: DBSession, redis: RedisClient) -> JSONResponse:
    try:
        async with timeout(READINESS_TIMEOUT):
            await db.execute(text("SELECT 1"))
            server_ready = await redis.ping()
    except (OSError, InterfaceError, PostgresError, RedisError, SQLAlchemyError):
        server_ready = False

    if server_ready:
        return JSONResponse(health_up)

    return JSONResponse(content=health_down, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, )
