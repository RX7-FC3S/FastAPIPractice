from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional, TYPE_CHECKING


from . import model

from services.basic_data.item.item_info.schema import ItemInfo
from services.inbound.inbound_order.inbound_order_header.schema import InboundOrderHeader


class InboundOrderDetail(DataSchemaBase):
    inbound_order_header: "InboundOrderHeader"
    seq: int
    item: "ItemInfo"

    quantity_of_pieces: int
    quantity_of_carton: Optional[int] = None
    quantity_of_pallet: Optional[int] = None


class Request:
    class AddInboundOrderDetail(SQLModel):
        inbound_order_header_id: int
        seq: int
        item_id: int
        quantity_of_pieces: int
        quantity_of_carton: Optional[int] = None
        quantity_of_pallet: Optional[int] = None


class Response:
    class AddInboundOrderDetail(ResponseBase[InboundOrderDetail]):
        pass
