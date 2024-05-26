from utils import as_advanced_query_and_order_schema
from common.response import as_response_data
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional


from . import model
from services.basic_data.business.stakeholder.schema import Stakeholder
from services.basic_data.business.order_type.schema import OrderType


class OrderType2(OrderType.select(include=["order_type_name"])):
    pass


class Sender(Stakeholder.select(include=["stakeholder_name", "contact", "phone"])):
    pass


class Receiver(Stakeholder.select(include=["stakeholder_name", "contact", "phone"])):
    pass


class ReceivingListHeader(DataSchemaBase):
    receiving_list_number: str
    related_order_number: Optional[str]
    order_type: OrderType2
    sender: Sender
    receiver: Receiver


class DBReceivingListHeader(ReceivingListHeader):
    order_type_id: int
    sender_id: int
    receiver_id: int


class Request:
    class AddReceivingListHeader(SQLModel):
        receiving_list_number: str
        related_order_number: Optional[str]
        order_type_id: int
        sender_id: int
        receiver_id: int

    class UpdateReceivingListHeader(SQLModel):
        id: int
        receiving_list_number: str
        related_order_number: Optional[str]
        order_type_id: int
        sender_id: int
        receiver_id: int

    @as_advanced_query_and_order_schema()
    class GetReceivingListHeaders(ReceivingListHeader):
        pass


class Response:
    @as_response_data()
    class AddReceivingListHeader(DBReceivingListHeader):
        pass

    @as_response_data()
    class DeleteReceivingListHeader(
        ReceivingListHeader.select(exclude=["sender", "receiver", "order_type"])
    ):
        pass

    @as_response_data()
    class UpdateReceivingListHeader(ReceivingListHeader):
        pass

    @as_response_data()
    class GetReceivingListHeaders(Page[ReceivingListHeader]):
        pass

    @as_response_data()
    class GetReceivingListHeaderById(DBReceivingListHeader):
        pass
