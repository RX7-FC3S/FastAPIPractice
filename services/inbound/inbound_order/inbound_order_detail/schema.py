from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase, as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional, TYPE_CHECKING


from . import model

from services.basic_data.item.item_info.schema import ItemInfo
from services.inbound.inbound_order.inbound_order_header.schema import (
    InboundOrderHeader,
)


class InboundOrderDetail(DataSchemaBase):
    inbound_order_header: "InboundOrderHeader"
    seq: int
    item: "ItemInfo"

    quantity_of_pieces: int
    quantity_of_carton: Optional[int] = None
    quantity_of_pallet: Optional[int] = None

class DBInboundOrderDetail(InboundOrderDetail):
    inbound_order_header_id: int
    item_id: int


class Request:
    class AddInboundOrderDetail(SQLModel):
        inbound_order_header_id: int
        item_id: int
        unit_id: int
        quantity: int

    @as_advanced_query_and_order_schema()
    class GetInboundOrderDetails(InboundOrderDetail):
        pass


class Response:
    @as_response_data()
    class AddInboundOrderDetail(InboundOrderDetail):
        pass

    @as_response_data()
    class DeleteInboundOrderDetail(DBInboundOrderDetail.select(exclude=['inbound_order_header', 'item'])):
        pass

    @as_response_data()
    class GetInboundOrderDetails(Page[InboundOrderDetail]):
        pass
    