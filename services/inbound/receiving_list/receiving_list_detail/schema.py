from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase, as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional, TYPE_CHECKING


from . import model

from services.basic_data.item.item_info.schema import ItemInfo
from services.basic_data.item.item_unit.schema import ItemUnit
from services.inbound.receiving_list.receiving_list_header.schema import (
    ReceivingListHeader,
)


class ReceivingListDetail(DataSchemaBase):
    receiving_list_header: "ReceivingListHeader"
    seq: int
    item_info: "ItemInfo"
    item_unit: "ItemUnit"
    quantity: int


class ReceivingListDetailWithoutHeader(DataSchemaBase):
    seq: int
    item_info: "ItemInfo"
    item_unit: "ItemUnit"
    quantity: int


class DBReceivingListDetail(ReceivingListDetail):
    receiving_list_header_id: int
    item_info_id: int


class Request:
    class AddReceivingListDetail(SQLModel):
        receiving_list_header_id: int
        item_info_id: int
        item_unit_id: int
        quantity: int

    @as_advanced_query_and_order_schema()
    class GetReceivingListDetails(DBReceivingListDetail):
        pass


class Response:
    @as_response_data()
    class AddReceivingListDetail(ReceivingListDetail):
        pass

    @as_response_data()
    class DeleteReceivingListDetail(
        DBReceivingListDetail.select(exclude=["receiving_list_header", "item_info"])
    ):
        pass

    @as_response_data()
    class GetReceivingListDetails(Page[ReceivingListDetail]):
        pass

    @as_response_data()
    class GetReceivingListDetailsWithoutHeader(Page[ReceivingListDetailWithoutHeader]):
        pass
