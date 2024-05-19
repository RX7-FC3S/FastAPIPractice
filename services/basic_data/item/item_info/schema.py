from utils import as_advanced_query_and_order_schema
from common.response import as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model

from services.basic_data.item.item_unit.model import ItemUint


class ItemInfo(DataSchemaBase):
    item_code: str
    item_name: str


class Request:
    class AddItemInfo(SQLModel):
        item_code: str
        item_name: str

    @as_advanced_query_and_order_schema()
    class GetItemInfos(ItemInfo):
        pass


class Response:
    @as_response_data()
    class AddItemInfo(ItemInfo):
        pass

    @as_response_data()
    class GetItemInfos(Page[ItemInfo]):
        pass
