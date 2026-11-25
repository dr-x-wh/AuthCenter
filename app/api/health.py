import random

from fastapi import APIRouter
from fastapi.responses import JSONResponse

api = APIRouter(prefix="/health", tags=["健康检查"])


@api.get("")
async def health() -> JSONResponse:
    num = random.randint(0, 9)
    if num != 0:
        return JSONResponse({"status": "UP"})
    else:
        return JSONResponse(content={"status": "DOWN", "message": "Internal component failure"}, status_code=503)


@api.get("/live")
async def health() -> JSONResponse:
    num = random.randint(0, 9)
    if num != 0:
        return JSONResponse({"status": "UP"})
    else:
        return JSONResponse(content={"status": "DOWN", "message": "Internal component failure"}, status_code=503)


@api.get("/ready")
async def health() -> JSONResponse:
    num = random.randint(0, 9)
    if num != 0:
        return JSONResponse({"status": "UP"})
    else:
        return JSONResponse(content={"status": "DOWN", "message": "Internal component failure"}, status_code=503)


@api.get("/startup")
async def health() -> JSONResponse:
    num = random.randint(0, 9)
    if num != 0:
        return JSONResponse({"status": "UP"})
    else:
        return JSONResponse(content={"status": "DOWN", "message": "Internal component failure"}, status_code=503)
