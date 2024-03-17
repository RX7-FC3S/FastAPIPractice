from typing import Any, TypeVar, Generic, Literal
from fastapi_pagination import Page
from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None


class Response(object):
    def __init__(self, success: bool, message: str, data: Any | None) -> None:
        self.success = success
        self.message = message
        self.data = data
