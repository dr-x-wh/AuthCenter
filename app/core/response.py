from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    data: T | None = None
    code: int = 0
    message: str = "success"
