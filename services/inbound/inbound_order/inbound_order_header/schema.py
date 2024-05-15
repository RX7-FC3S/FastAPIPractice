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


class InboundOrderHeader(DataSchemaBase):
    inbound_order_number: str
    related_order_number: Optional[str]
    order_type: OrderType2
    sender: Sender
    receiver: Receiver


class Request:
    class AddInboundOrderHeader(SQLModel):
        inbound_order_number: str
        related_order_number: Optional[str]
        order_type_id: int
        sender_id: int
        receiver_id: int
    
    @as_advanced_query_and_order_schema()
    class GetInboundOrderHeaders(InboundOrderHeader):
        pass


class Response:
    @as_response_data()
    class AddInboundOrderHeader(InboundOrderHeader):
        id: int
        order_type_id: int
        sender_id: int
        receiver_id: int
    
    @as_response_data()
    class DeleteInboundOrderHeader(InboundOrderHeader.select(exclude=['sender', 'receiver', 'order_type'])):
        id: int
        order_type_id: int
        sender_id: int
        receiver_id: int

    @as_response_data()
    class GetInboundOrderHeaders(Page[InboundOrderHeader]):
        pass

    @as_response_data()
    class GetInboundOrderHeaderById(InboundOrderHeader):
        id: int
        order_type_id: int
        sender_id: int
        receiver_id: int

