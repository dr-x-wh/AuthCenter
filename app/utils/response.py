from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    data: T | None = None
    code: int = 0
    message: str = "success"
