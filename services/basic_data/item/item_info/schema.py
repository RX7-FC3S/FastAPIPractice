from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model


class ItemInfo(DataSchemaBase):
    item_code: str
    item_name: str
    base_unit: str


class Request:
    class AddItem(ItemInfo):
        pass

    @as_advanced_query_and_order_schema()
    class GetItems(ItemInfo):
        pass


class Response:
    class AddItem(ResponseBase[ItemInfo]):
        pass

    class GetItems(ResponseBase[Page[ItemInfo]]):
        pass
