from fastapi import APIRouter, status

from app.core.errors import BusinessError

router = APIRouter(tags=["认证"])


@router.get("/login")
async def login() -> None:
    raise BusinessError("尚未实现")
