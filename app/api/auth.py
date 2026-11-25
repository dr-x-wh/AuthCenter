from fastapi import APIRouter

from app.core.config import setting
from app.utils.response import Result
from app.logger import logger

api = APIRouter(tags=["认证"])


@api.get("/login")
async def login() -> Result:
    logger.info(setting.DATABASE_URL)
    return Result({"name": "xwh", "url": setting.REDIS_URL})
