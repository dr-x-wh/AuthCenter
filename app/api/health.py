from asyncio import timeout

from asyncpg import PostgresError
from fastapi import APIRouter, Response, status
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .deps import DBSession, RedisClient

router = APIRouter(prefix="/health", tags=["健康检查"])
READINESS_TIMEOUT = 3


@router.get("")
@router.get("/live")
@router.get("/startup")
async def live() -> dict[str, str]:
    return {"status": "UP"}


@router.get("/ready", responses={503: {"description": "依赖服务不可用"}})
async def ready(db: DBSession, redis: RedisClient, response: Response) -> dict[str, str]:
    try:
        async with timeout(READINESS_TIMEOUT):
            await db.execute(text("SELECT 1"))
            await redis.ping()
    except (OSError, PostgresError, RedisError, SQLAlchemyError):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "DOWN", "message": "Internal component failure"}

    return {"status": "UP"}
