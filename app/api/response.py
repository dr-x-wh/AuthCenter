from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    data: T | None = None
    code: int = 0
    message: str = "success"


def error_response(
    status_code: int,
    message: str,
    *,
    data: Any = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    result = Result(data=data, code=status_code, message=message)
    return JSONResponse(result.model_dump(mode="json"), status_code=status_code, headers=headers)
