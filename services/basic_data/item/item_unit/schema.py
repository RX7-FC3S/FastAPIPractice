from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model


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

    class GetItemUnitsByItemCode(SQLModel):
        item_code: str


class Response:
    class AddItemUnit(ItemUnit):
        pass

    class GetItemUnitsByItemCode(ResponseBase[list[ItemUnit]]):
        pass
