from typing import Generic, TypeVar, Any, Mapping

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")
DEFAULT_CODE = 0
DEFAULT_MESSAGE = "成功"


class Result(BaseModel, Generic[T]):
    data: T | None = None
    code: int = DEFAULT_CODE
    message: str = DEFAULT_MESSAGE


def to_response(data: Any = None, code: int = DEFAULT_CODE, message: str = DEFAULT_MESSAGE) -> JSONResponse:
    result = Result[Any](data=data, code=code, message=message)
    return JSONResponse(result.model_dump(mode="json"))


def error_response(status_code: int, message: str, *, data: Any = None, headers: Mapping[str, str] | None = None) -> JSONResponse:
    result = Result(data=data, code=status_code, message=message)
    return JSONResponse(result.model_dump(mode="json"), status_code=status_code, headers=headers)
