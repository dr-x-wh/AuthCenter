from asyncio import timeout
from typing import Literal

from asyncpg import InterfaceError, PostgresError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..deps import DBSession, RedisClient

router = APIRouter(prefix="/health", tags=["健康检查"])
READINESS_TIMEOUT = 3


class HealthUp(BaseModel):
    status: Literal["UP"]


class HealthDown(BaseModel):
    status: Literal["DOWN"]
    message: str


@router.get("")
@router.get("/live")
@router.get("/startup")
async def live() -> HealthUp:
    return HealthUp(status="UP")


@router.get(
    "/ready",
    response_model=HealthUp,
    responses={503: {"model": HealthDown, "description": "依赖服务不可用"}},
)
async def ready(db: DBSession, redis: RedisClient) -> HealthUp | JSONResponse:
    try:
        async with timeout(READINESS_TIMEOUT):
            await db.execute(text("SELECT 1"))
            redis_ready = await redis.ping()
    except (OSError, InterfaceError, PostgresError, RedisError, SQLAlchemyError):
        redis_ready = False

    if redis_ready:
        return HealthUp(status="UP")

    return JSONResponse(
        content=HealthDown(status="DOWN", message="Internal component failure").model_dump(),
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
