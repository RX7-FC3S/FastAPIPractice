from pydantic import BaseModel
from typing import Union, Any, TypeVar, Generic
from fastapi_pagination import Page

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    status: bool
    message: str
    data: T | list[T] | Page[T] | None


class Response(object):
    def __init__(self, status: bool, message: str, data: Any | None) -> None:
        self.status = status
        self.message = message
        self.data = data
