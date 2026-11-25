from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .response import Result


async def handle_http_error(_request: Request, _exc: HTTPException) -> Result:
    return Result(code=-1, message="http异常")


async def handle_validation_error(_request: Request, _exc: RequestValidationError, ) -> Result:
    return Result(code=-2, message="参数校验异常")


async def handle_unexpected_error(_request: Request, _exc: Exception) -> Result:
    return Result(code=-99, message="系统未知错误")


exception_handlers = {RequestValidationError: handle_validation_error, HTTPException: handle_http_error, Exception: handle_unexpected_error, }
