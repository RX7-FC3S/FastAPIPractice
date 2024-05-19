from utils import as_advanced_query_and_order_schema
from common.response import as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel, Sequence

from . import model

from services.basic_data.item.item_info.model import ItemInfo


class ItemUnit(DataSchemaBase):
    unit_type: int
    unit_name: str

    conversion_quantity: int


class Request:
    class AddItemUnit(SQLModel):
        item_id: int
        unit_type: int
        unit_name: str
        conversion_quantity: int

    @as_advanced_query_and_order_schema()
    class GetItemUnits(ItemUnit):
        item_id: int


class Response:
    @as_response_data()
    class AddItemUnit(ItemUnit):
        pass

    @as_response_data()
    class GetItemUnits(Page[ItemUnit]):
        pass

    @as_response_data()
    class GetItemUnitsByItemId(Page[ItemUnit]):
        pass
