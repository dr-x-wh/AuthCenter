from collections.abc import Mapping
from typing import Any, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")
DEFAULT_CODE = 0
DEFAULT_MESSAGE = "成功"


class Result[T](BaseModel):
    data: T | None = None
    code: int = DEFAULT_CODE
    message: str = DEFAULT_MESSAGE


def make_result(data: Any = None, code: int = DEFAULT_CODE, message: str = DEFAULT_MESSAGE) -> JSONResponse:
    result = Result[Any](code=code, data=data, message=message)
    return JSONResponse(result.model_dump(mode="json"))


def make_response(
    message: str,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    data: Any = None,
) -> JSONResponse:
    result = Result(code=-99, data=data, message=message)
    return JSONResponse(result.model_dump(mode="json"), status_code=status_code, headers=headers)
