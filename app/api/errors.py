from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.utils import is_body_allowed_for_status_code
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from .response import Result, error_response


class ValidationIssue(BaseModel):
    loc: tuple[str | int, ...]
    msg: str
    type: str


async def handle_http_error(_request: Request, exc: HTTPException) -> Response:
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=exc.headers)
    if isinstance(exc.detail, str):
        return error_response(exc.status_code, exc.detail, headers=exc.headers)
    return error_response(
        exc.status_code,
        "Request failed",
        data=exc.detail,
        headers=exc.headers,
    )


async def handle_validation_error(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    issues = [
        ValidationIssue(loc=error["loc"], msg=error["msg"], type=error["type"])
        for error in exc.errors()
    ]
    return error_response(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "Request validation failed",
        data=issues,
    )


async def handle_unexpected_error(_request: Request, _exc: Exception) -> JSONResponse:
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")


exception_handlers = {
    HTTPException: handle_http_error,
    RequestValidationError: handle_validation_error,
    Exception: handle_unexpected_error,
}

error_responses = {
    422: {"model": Result[list[ValidationIssue]], "description": "请求校验失败"},
    500: {"model": Result[None], "description": "内部服务异常"},
}
