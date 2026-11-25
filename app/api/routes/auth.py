from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(tags=["认证"])


class LoginUnavailable(BaseModel):
    detail: str


@router.get(
    "/login",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    response_model=LoginUnavailable,
    response_description="认证功能尚未实现",
)
async def login() -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login is not implemented",
    )
