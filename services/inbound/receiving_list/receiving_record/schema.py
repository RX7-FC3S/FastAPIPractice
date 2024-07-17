from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional


from services.inbound.receiving_list.receiving_list_detail.schema import (
    ReceivingListDetail,
)


class ReceivingRecord(DataSchemaBase):
    receiving_list_detail: "ReceivingListDetail"
    quantity: int
    remark: str


class DBReceivingListDetail(ReceivingListDetail):
    receiving_list_detail_id: int


class RequestAddReceivingRecord(SQLModel):
    id: int
    receiving_quantity: int
    pallet_number: Optional[str] = None
    carton_number: Optional[str] = None
    remark: Optional[str] = None


class RequestAddReceivingRecords(SQLModel):
    items: list[RequestAddReceivingRecord]


class Request:
    class AddReceivingRecord(SQLModel):
        receiving_list_detail_id: int
        quantity: int
        remark: str

    @as_advanced_query_and_order_schema()
    class GetReceivingListDetails(ReceivingListDetail):
        pass


class Response:
    class AddReceivingRecord(ResponseBase[DBReceivingListDetail]):
        pass

    class GetReceivingListDetails(ResponseBase[Page[ReceivingListDetail]]):
        pass
