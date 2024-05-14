from pydantic import BaseModel, create_model
from typing import Any, TypeVar, Generic
from sqlmodel.main import FieldInfo
from sqlmodel import SQLModel

T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None


def as_response_data():
    def wrapper(cls: type[SQLModel]) -> type[SQLModel]:
        return create_model(f'{cls.__name__}AsResponse', __base__=None, **{
            'success': (bool, FieldInfo(required=True)),
            'message': (str, FieldInfo(required=True)),
            'data': (cls, FieldInfo(required=True))
        }) # type: ignore
    return wrapper



class Response(object):
    def __init__(self, success: bool, message: str, data: Any | None) -> None:
        self.success = success
        self.message = message
        self.data = data
