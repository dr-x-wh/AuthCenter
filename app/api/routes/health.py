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
from ..response import Result, error_response

router = APIRouter(prefix="/health", tags=["健康检查"])
READINESS_TIMEOUT = 3


class HealthUp(BaseModel):
    status: Literal["UP"]


class HealthDown(BaseModel):
    status: Literal["DOWN"]


@router.get("")
@router.get("/live")
@router.get("/startup")
async def live() -> Result[HealthUp]:
    return Result(data=HealthUp(status="UP"))


@router.get(
    "/ready",
    response_model=Result[HealthUp],
    responses={503: {"model": Result[HealthDown], "description": "依赖服务不可用"}},
)
async def ready(db: DBSession, redis: RedisClient) -> Result[HealthUp] | JSONResponse:
    try:
        async with timeout(READINESS_TIMEOUT):
            await db.execute(text("SELECT 1"))
            redis_ready = await redis.ping()
    except (OSError, InterfaceError, PostgresError, RedisError, SQLAlchemyError):
        redis_ready = False

    if redis_ready:
        return Result(data=HealthUp(status="UP"))

    return error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "Internal component failure",
        data=HealthDown(status="DOWN"),
    )
