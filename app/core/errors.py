from http.client import responses as HTTP_STATUS_DETAILS

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException

from .logging import logger
from .response import make_response, make_result

HTTP_ERROR_MESSAGES = {
    400: "请求有误",
    401: "需要身份认证",
    403: "无权访问",
    404: "未找到请求的资源",
    405: "不支持此请求方法",
    409: "请求与资源当前状态冲突",
    413: "请求内容过大",
    415: "不支持此请求内容类型",
    429: "请求过于频繁",
    500: "服务器内部错误",
    501: "请求的功能尚未实现",
    502: "上游服务响应异常",
    503: "服务暂时不可用",
    504: "等待上游服务响应超时",
}


class BusinessError(Exception):
    pass


async def handle_business_error(_request: Request, exc: BusinessError) -> Response:
    return make_result(code=-1, message=str(exc))


async def handle_http_error(_request: Request, exc: HTTPException) -> Response:
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=exc.headers)
    detail = exc.detail
    message = HTTP_ERROR_MESSAGES.get(exc.status_code, "请求处理失败")
    if isinstance(detail, str) and detail != HTTP_STATUS_DETAILS.get(exc.status_code, ""):
        message = detail
    return make_response(message=message, status_code=exc.status_code, headers=exc.headers)


async def handle_validation_error(_request: Request, _exc: RequestValidationError) -> JSONResponse:
    return make_response(message="请求参数校验失败", status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)


async def handle_unexpected_error(_request: Request, exc: Exception) -> JSONResponse:
    logger.error("处理请求时发生未捕获的异常", exc_info=exc)
    return make_response(message="服务器内部错误", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


exception_handlers = {
    BusinessError: handle_business_error,
    RequestValidationError: handle_validation_error,
    HTTPException: handle_http_error,
    Exception: handle_unexpected_error,
}
