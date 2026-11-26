from fastapi import APIRouter

from app.core.errors import BusinessError

router = APIRouter(tags=["认证"])


@router.get("/text")
async def text() -> None:
    raise BusinessError("尚未实现")
