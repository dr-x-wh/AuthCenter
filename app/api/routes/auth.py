from fastapi import APIRouter, HTTPException, status

from app.core.response import Result

router = APIRouter(tags=["认证"])


@router.get(
    "/login",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    response_model=Result[None],
    response_description="认证功能尚未实现",
)
async def login() -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login is not implemented",
    )
