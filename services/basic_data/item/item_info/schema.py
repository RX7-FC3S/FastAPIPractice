from utils import as_advanced_query_and_order_schema
from common.response import as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model


class ItemInfo(DataSchemaBase):
    item_code: str
    item_name: str


class Request:
    class AddItem(ItemInfo):
        pass

    @as_advanced_query_and_order_schema()
    class GetItems(ItemInfo):
        pass


class Response:
    @as_response_data()
    class AddItem(ItemInfo):
        pass

    @as_response_data()
    class GetItems(Page[ItemInfo]):
        pass
