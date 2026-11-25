from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["认证"])


@router.get("/login", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def login() -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login is not implemented",
    )
