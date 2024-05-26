from utils import as_advanced_query_and_order_schema
from common.response import as_response_data, ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel, Sequence
from typing import Any, List

from . import model

from services.basic_data.item.item_info.model import ItemInfo


class ItemUnit(DataSchemaBase):
    unit_type: int
    unit_name: str

    conversion_quantity: int

class DBItemUnit(ItemUnit):
    item_info_id: int


class Request:
    class AddItemUnit(SQLModel):
        item_info_id: int
        unit_type: int
        unit_name: str
        conversion_quantity: int

    @as_advanced_query_and_order_schema()
    class GetItemUnits(ItemUnit):
        item_info_id: int


from typing import Generic, TypeVar

T = TypeVar('T')

class DataList(list, Generic[T]):
    pass


class Response:
    @as_response_data()
    class AddItemUnit(ItemUnit):
        pass

    @as_response_data()
    class GetItemUnits(Page[ItemUnit]):
        pass

    
    class GetItemUnitsByItemId(ResponseBase[list[DBItemUnit]]):
        pass
        
